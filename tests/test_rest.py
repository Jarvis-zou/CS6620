import os
import pytest
import requests
import boto3
from botocore.exceptions import NoCredentialsError
import json

api_url = os.getenv('API_URL', 'http://localhost:5000')
endpoint_url = 'http://localstack:4566'
bucket_name = 'my-test-bucket'


@pytest.fixture(scope='module')
def test_client():
    yield requests.Session()


def get_s3_object(key):
    try:
        s3_client = boto3.client('s3',
                                 endpoint_url=endpoint_url,
                                 region_name='us-east-1',
                                 aws_access_key_id='test',
                                 aws_secret_access_key='test')
        s3_object = s3_client.get_object(Bucket=bucket_name, Key=key)
        return json.loads(s3_object['Body'].read().decode('utf-8'))
    except s3_client.exceptions.NoSuchKey:
        return None
    except NoCredentialsError:
        pytest.fail("AWS credentials not found")


def get_dynamodb_item(item_id):
    try:
        dynamodb = boto3.resource('dynamodb',
                                  endpoint_url=endpoint_url,
                                  region_name='us-east-1',
                                  aws_access_key_id='test',
                                  aws_secret_access_key='test')
        table = dynamodb.Table('MyTestTable')
        response = table.get_item(Key={'id': item_id})
        return response.get('Item')
    except NoCredentialsError:
        pytest.fail("AWS credentials not found")


def test_create_item(test_client):
    response = test_client.post(f'{api_url}/items', json={'id': '123', 'data': 'test data'})
    assert response.status_code == 201
    assert response.json() == {'id': '123', 'data': 'test data'}

    s3_data = get_s3_object('123')
    assert s3_data == {'id': '123', 'data': 'test data'}

    dynamodb_item = get_dynamodb_item('123')
    assert dynamodb_item == {'id': '123', 'data': 'test data'}


def test_get_item(test_client):
    response = test_client.get(f'{api_url}/items/123')
    assert response.status_code == 200
    assert response.json() == {'id': '123', 'data': 'test data'}

    s3_data = get_s3_object('123')
    assert s3_data == {'id': '123', 'data': 'test data'}

    dynamodb_item = get_dynamodb_item('123')
    assert dynamodb_item == {'id': '123', 'data': 'test data'}


def test_get_item_not_found(test_client):
    response = test_client.get(f'{api_url}/items/999')
    assert response.status_code == 404
    assert response.json() == {'error': 'Item not found'}


def test_get_item_no_parameters(test_client):
    response = test_client.get(f'{api_url}/items/')
    assert response.status_code == 404


def test_get_item_incorrect_parameters(test_client):
    response = test_client.get(f'{api_url}/items/?wrong_param=wrong')
    assert response.status_code == 404


def test_post_duplicate_item(test_client):
    response = test_client.post(f'{api_url}/items', json={'id': '123', 'data': 'duplicate data'})
    assert response.status_code == 409


def test_update_item(test_client):
    response = test_client.put(f'{api_url}/items/123', json={'data': 'updated data'})
    assert response.status_code == 200
    assert response.json() == {'id': '123', 'data': 'updated data'}

    s3_data = get_s3_object('123')
    assert s3_data == {'id': '123', 'data': 'updated data'}

    dynamodb_item = get_dynamodb_item('123')
    assert dynamodb_item == {'id': '123', 'data': 'updated data'}


def test_update_item_not_found(test_client):
    response = test_client.put(f'{api_url}/items/999', json={'data': 'new data'})
    assert response.status_code == 404


def test_delete_item(test_client):
    response = test_client.delete(f'{api_url}/items/123')
    assert response.status_code == 200
    assert response.json() == {'result': 'Item deleted'}

    s3_data = get_s3_object('123')
    assert s3_data is None

    dynamodb_item = get_dynamodb_item('123')
    assert dynamodb_item is None


def test_delete_item_not_found(test_client):
    response = test_client.delete(f'{api_url}/items/999')
    assert response.status_code == 404
