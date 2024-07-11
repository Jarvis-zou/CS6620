import requests

BASE_URL = 'http://localhost:5000/items'

def test_create_item():
    response = requests.post(BASE_URL, json={'id': '1', 'name': 'Test Item'})
    assert response.status_code == 201

def test_get_item():
    response = requests.get(f'{BASE_URL}/1')
    assert response.status_code == 200
    assert response.json()['name'] == 'Test Item'

def test_update_item():
    response = requests.put(f'{BASE_URL}/1', json={'name': 'Updated Item'})
    assert response.status_code == 200
    response = requests.get(f'{BASE_URL}/1')
    assert response.json()['name'] == 'Updated Item'

def test_delete_item():
    response = requests.delete(f'{BASE_URL}/1')
    assert response.status_code == 200
    response = requests.get(f'{BASE_URL}/1')
    assert response.status_code == 404
