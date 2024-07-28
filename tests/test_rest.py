import os
print("Current working directory: ", os.getcwd())
import pytest
import boto3
from botocore.exceptions import ClientError
from REST.rest import app, create_dynamodb_table, create_s3_bucket
import json

os.environ['AWS_ACCESS_KEY_ID'] = 'test'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'test'

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
bucket_name = 'my-test-bucket'

@pytest.fixture(scope='module')
def test_client():
    create_dynamodb_table()
    create_s3_bucket()

    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client

def test_create_item(test_client):
    response = test_client.post('/items', json={'id': '123', 'data': 'test data'})
    assert response.status_code == 201
    assert response.json == {'id': '123', 'data': 'test data'}

    table = dynamodb.Table(table_name)
    response = table.get_item(Key={'id': '123'})
    assert 'Item' in response
    assert response['Item'] == {'id': '123', 'data': 'test data'}

    response = s3.get_object(Bucket=bucket_name, Key='123')
    s3_data = json.loads(response['Body'].read().decode('utf-8'))
    assert s3_data == {'id': '123', 'data': 'test data'}

def test_get_item(test_client):
    response = test_client.get('/items/123')
    assert response.status_code == 200
    assert response.json == {'id': '123', 'data': 'test data'}

def test_get_item_not_found(test_client):
    response = test_client.get('/items/999')
    assert response.status_code == 404
    assert response.json == {'error': 'Item not found'}

def test_get_item_no_parameters(test_client):
    response = test_client.get('/items/')
    assert response.status_code == 404

def test_get_item_incorrect_parameters(test_client):
    response = test_client.get('/items/?wrong_param=wrong')
    assert response.status_code == 404

def test_post_duplicate_item(test_client):
    # First POST request
    test_client.post('/items', json={'id': '123', 'data': 'test data'})
    # Duplicate POST request
    response = test_client.post('/items', json={'id': '123', 'data': 'duplicate data'})
    assert response.status_code == 409  # Conflict

def test_update_item(test_client):
    response = test_client.put('/items/123', json={'id': '123', 'data': 'updated data'})
    assert response.status_code == 200
    assert response.json == {'id': '123', 'data': 'updated data'}

    table = dynamodb.Table(table_name)
    response = table.get_item(Key={'id': '123'})
    assert 'Item' in response
    assert response['Item'] == {'id': '123', 'data': 'updated data'}

    response = s3.get_object(Bucket=bucket_name, Key='123')
    s3_data = json.loads(response['Body'].read().decode('utf-8'))
    assert s3_data == {'id': '123', 'data': 'updated data'}

def test_update_item_not_found(test_client):
    response = test_client.put('/items/999', json={'id': '999', 'data': 'new data'})
    assert response.status_code == 404  # Assuming API returns 404 if the item does not exist

def test_delete_item(test_client):
    response = test_client.delete('/items/123')
    assert response.status_code == 200
    assert response.json == {'result': 'Item deleted'}

    table = dynamodb.Table(table_name)
    response = table.get_item(Key={'id': '123'})
    assert 'Item' not in response

    with pytest.raises(ClientError) as e:
        response = s3.get_object(Bucket=bucket_name, Key='123')
    assert e.value.response['Error']['Code'] == 'NoSuchKey'

def test_delete_item_not_found(test_client):
    response = test_client.delete('/items/999')
    assert response.status_code == 404  # Assuming API returns 404 if the item does not exist
