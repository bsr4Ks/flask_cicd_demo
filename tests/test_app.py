import pytest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app
from unittest.mock import patch

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200

def test_catfacts_get(client):
    response = client.get('/catfacts')
    assert response.status_code == 200


@patch('requests.get')
def test_catfacts_post(mock_get, client):
    mock_get.return_value.json.return_value = {"fact": "Cats purr to communicate."}
    response = client.post('/catfacts')
    assert b"Cats purr to communicate." in response.data

@patch('requests.get')
def test_dogimages_post(mock_get, client):
    mock_get.return_value.json.return_value = {
        "status": "success",
        "message": "https://example.com/dog.jpg"
    }
    response = client.post('/dogimages')
    assert b"https://example.com/dog.jpg" in response.data
