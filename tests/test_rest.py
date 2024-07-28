import os
import pytest
import requests

api_url = os.getenv('API_URL', 'http://localhost:5000')

@pytest.fixture(scope='module')
def test_client():
    yield requests.Session()

def test_create_item(test_client):
    response = test_client.post(f'{api_url}/items', json={'id': '123', 'data': 'test data'})
    assert response.status_code == 201
    assert response.json() == {'id': '123', 'data': 'test data'}

def test_get_item(test_client):
    response = test_client.get(f'{api_url}/items/123')
    assert response.status_code == 200
    assert response.json() == {'id': '123', 'data': 'test data'}

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

def test_update_item_not_found(test_client):
    response = test_client.put(f'{api_url}/items/999', json={'data': 'new data'})
    assert response.status_code == 404

def test_delete_item(test_client):
    response = test_client.delete(f'{api_url}/items/123')
    assert response.status_code == 200
    assert response.json() == {'result': 'Item deleted'}

def test_delete_item_not_found(test_client):
    response = test_client.delete(f'{api_url}/items/999')
    assert response.status_code == 404

