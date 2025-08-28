from http.client import responses
import pytest
from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)

def test_search1():
    response = client.post('/semanticSearch',json={
        "message":"bluetooth head phones"
    })
    assert response.status_code == 200
    data = response.json()

    # Check structure
    assert "results" in data
    assert len(data["results"]) > 0, "Semantic search returned no results"


def test_search2():
    response = client.post('/semanticSearch',json={
        "message":"earphones"
    })
    assert response.status_code == 200
    data = response.json()

    # Check structure
    assert "results" in data
    assert len(data["results"]) > 0, "Semantic search returned no results"



def test_search3():
    # Arrange
    payload = {"message": "bluetooth head phones"}

    # Act
    response = client.post('/semanticSearch', json=payload)

    # Status code
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"

    data = response.json()

    # Structure
    assert "results" in data, "'results' key is missing in response JSON"
    assert isinstance(data["results"], list), "'results' should be a list"
    assert len(data["results"]) > 0, "Expected at least one search result"

    first_result = data["results"][0]

    # Content fields
    assert "content" in first_result, "Missing 'content' in first result"
    assert "metadata" in first_result, "Missing 'metadata' in first result"
    assert "score" in first_result, "Missing 'score' in first result"

    # Content relevance
    assert "headphone" in first_result["content"].lower(), \
        f"Expected 'headphone' in content, got: {first_result['content']}"

    # Assert: Score is a float and within reasonable range
    assert isinstance(first_result["score"], float), "Score should be a float"
    assert first_result["score"] == pytest.approx(0.44, rel=0.3), \
        f"Score is not close to expected (~0.44). Got: {first_result['score']}"


def test_prediction():
    response = client.post('/predict',json={
    "Price": 40.90,
    "Discount": 0.00,
    "Category_Amino_Acid": 0,
    "Category_Fat_Burner": 0,
    "Category_Herbal": 0,
    "Category_Hydration": 0,
    "Category_Mineral": 0,
    "Category_Omega": 0,
    "Category_Performance": 0,
    "Category_Protein": 1,
    "Category_Sleep_Aid": 0,
    "Category_Vitamin": 0})
    assert response.status_code == 200
    data = response.json()

    assert "res" in data
    assert len(data["res"]) > 0, "prediction returned no results"
