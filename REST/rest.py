import boto3
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# 添加了 AWS 凭证参数
dynamodb = boto3.resource('dynamodb',
                          endpoint_url='http://localhost:4566',
                          region_name='us-east-1',
                          aws_access_key_id='test',
                          aws_secret_access_key='test')
s3 = boto3.client('s3',
                  endpoint_url='http://localhost:4566',
                  region_name='us-east-1',
                  aws_access_key_id='test',
                  aws_secret_access_key='test')

table_name = 'MyTestTable'
bucket_name = 'my-test-bucket'  # 使用有效的存储桶名称


def create_dynamodb_table():
    try:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
    except dynamodb.meta.client.exceptions.ResourceInUseException:
        pass


def create_s3_bucket():
    try:
        s3.create_bucket(Bucket=bucket_name)
    except s3.exceptions.BucketAlreadyOwnedByYou:
        pass


@app.before_request
def setup():
    create_dynamodb_table()
    create_s3_bucket()


@app.route('/items', methods=['POST'])
def create_item():
    item = request.json
    table = dynamodb.Table(table_name)

    # Check if item already exists
    response = table.get_item(Key={'id': item['id']})
    if 'Item' in response:
        return jsonify({'error': 'Item already exists'}), 409

    table.put_item(Item=item)
    s3.put_object(Bucket=bucket_name, Key=item['id'], Body=json.dumps(item))
    return jsonify(item), 201


@app.route('/items/<item_id>', methods=['GET'])
def get_item(item_id):
    table = dynamodb.Table(table_name)
    response = table.get_item(Key={'id': item_id})
    if 'Item' in response:
        return jsonify(response['Item']), 200
    else:
        return jsonify({'error': 'Item not found'}), 404


@app.route('/items', methods=['GET'])
def get_item_no_parameters():
    return jsonify({'error': 'Item ID is required'}), 400


@app.route('/items/<item_id>', methods=['PUT'])
def update_item(item_id):
    table = dynamodb.Table(table_name)
    response = table.get_item(Key={'id': item_id})
    if 'Item' not in response:
        return jsonify({'error': 'Item not found'}), 404

    item = request.json
    table.update_item(
        Key={'id': item_id},
        UpdateExpression="set #data=:d",
        ExpressionAttributeValues={':d': item['data']},
        ExpressionAttributeNames={"#data": "data"},
        ReturnValues="UPDATED_NEW"
    )
    s3.put_object(Bucket=bucket_name, Key=item_id, Body=json.dumps(item))
    return jsonify(item), 200


@app.route('/items/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    table = dynamodb.Table(table_name)
    response = table.get_item(Key={'id': item_id})
    if 'Item' not in response:
        return jsonify({'error': 'Item not found'}), 404

    table.delete_item(Key={'id': item_id})
    s3.delete_object(Bucket=bucket_name, Key=item_id)
    return jsonify({'result': 'Item deleted'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
