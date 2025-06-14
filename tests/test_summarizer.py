from fastapi.testclient import TestClient
from app.main import app
import pytest
from unittest.mock import patch


client = TestClient(app)

@pytest.fixture
def mock_summarizer(monkeypatch):
    def fake_summarize(text):
        return "Mocked summary"

    monkeypatch.setattr("app.main.summarize_text", fake_summarize)


@patch("app.api.summarizer.summarizer_service")
def test_summarize_success(mock_service):
    mock_service.is_ready.return_value = True
    mock_service.summarize.return_value = "Mocked summary"

    response = client.post("/api/summarize", json={"text": "Hello"})

    assert response.status_code == 200
    assert response.json() == {"summary": "Mocked summary"}