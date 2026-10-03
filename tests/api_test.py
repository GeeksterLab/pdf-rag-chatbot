"""
GET /health → return 200
POST /login → return a token
POST /predict → without token return 401
POST /predict → with allowed token return a prediction

"""

# ╔════════════════════════════════════════════════════════════╗
# ║ 🚚 IMPORTS
# ╚════════════════════════════════════════════════════════════╝
import pytest
from fastapi.testclient import TestClient
from api.app import app


# TestClient + lifespan = need manager context
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "OK",
        "app": "medical__rag_chatbot",
        "description": "Document-grounded assistant that retrieves relevant chunks, cites its sources and refuses to invent an answer when the evidence is missing.",
        "version": "0.1.0",
    }
