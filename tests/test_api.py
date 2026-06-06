import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_login_page(client):
    rv = client.get('/')
    assert rv.status_code == 200

def test_login_success(client):
    rv = client.post('/', data={'username': 'admin', 'password': 'admin'})
    assert rv.status_code == 302

def test_login_wrong(client):
    rv = client.post('/', data={'username': 'admin', 'password': 'salah'})
    assert rv.status_code == 200