import pytest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app
from unittest.mock import patch

FLASK_SECRET_KEY=fbb60b6a4c8b457f061f60098608e8cce718c45b5c2db279
app.secret_key = FLASK_SECRET_KEY


def login(client, username='admin', password='secret'):
    return client.post('/login', data={
        'username': username,
        'password': password
    }, follow_redirects=True)

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def logged_in_client(client):
    login(client)
    return client


def test_home_page(logged_in_client):
    response = logged_in_client.get('/')
    assert response.status_code == 200

def test_catfacts_get(logged_in_client):
    response = logged_in_client.get('/catfacts')
    assert response.status_code == 200


@patch('requests.get')
def test_catfacts_post(mock_get, logged_in_client):
    mock_get.return_value.json.return_value = {"fact": "Cats purr to communicate."}
    response = logged_in_client.post('/catfacts')
    assert b"Cats purr to communicate." in response.data

@patch('requests.get')
def test_dogimages_post(mock_get, logged_in_client):
    mock_get.return_value.json.return_value = {
        "status": "success",
        "message": "https://example.com/dog.jpg"
    }
    response = logged_in_client.post('/dogimages')
    assert b"https://example.com/dog.jpg" in response.data
