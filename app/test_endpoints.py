from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Have to name the test function with 'test_' prefix for pytest to recognize it

def test_get_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers['content-type']
    assert "Code On!" in response.text
    assert "MadhushankhaDeS" in response.text


def test_post_home():
    response = client.post("/")
    assert response.status_code == 200
    assert "application/json" in response.headers['content-type']
    assert response.json() == {"message": "Welcome to the FastAPI application!"}
