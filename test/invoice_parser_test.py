import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_parse_invoice_existing_file():
    response = client.get("/parse-invoice/?file_name=invoice1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_parse_invoice_non_existing_file():
    response = client.get("/parse-invoice/?file_name=non_existing_invoice")
    assert response.status_code == 422  


def test_parse_invoice_invalid_content():
    response = client.get("/parse-invoice/?file_name=invoice_invalid")
    assert response.status_code == 200
    assert response.json() == [] 
