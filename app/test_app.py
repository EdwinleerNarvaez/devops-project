import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200

def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'ok'

def test_get_products(client):
    response = client.get('/products')
    assert response.status_code == 200
    assert 'products' in response.json

def test_create_product(client):
    response = client.post('/products', json={'name': 'Monitor', 'price': 300})
    assert response.status_code == 201
    assert response.json['name'] == 'Monitor'

def test_create_product_invalid(client):
    response = client.post('/products', json={})
    assert response.status_code == 400

def test_get_product_not_found(client):
    response = client.get('/products/9999')
    assert response.status_code == 404
