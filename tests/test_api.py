from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["application"] == "Fibonacci API"


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "UP"
    }


def test_ready():
    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json() == {
        "status": "READY"
    }


def test_live():
    response = client.get("/live")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ALIVE"
    }


def test_fibonacci_zero():
    response = client.get("/fibonacci?n=0")

    assert response.status_code == 200
    assert response.json() == {
        "n": 0,
        "value": 0
    }


def test_fibonacci_one():
    response = client.get("/fibonacci?n=1")

    assert response.status_code == 200
    assert response.json() == {
        "n": 1,
        "value": 1
    }


def test_fibonacci_ten():
    response = client.get("/fibonacci?n=10")

    assert response.status_code == 200
    assert response.json() == {
        "n": 10,
        "value": 55
    }


def test_fibonacci_twenty():
    response = client.get("/fibonacci?n=20")

    assert response.status_code == 200
    assert response.json() == {
        "n": 20,
        "value": 6765
    }


def test_negative_input():
    response = client.get("/fibonacci?n=-1")

    # FastAPI validation (Query(ge=0)) returns HTTP 422
    assert response.status_code == 422


def test_invalid_input():
    response = client.get("/fibonacci?n=abc")

    assert response.status_code == 422


def test_missing_parameter():
    response = client.get("/fibonacci")

    assert response.status_code == 422