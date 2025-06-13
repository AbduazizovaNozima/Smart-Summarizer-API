import pytest

def test_summarize_success(client, mock_summarizer):
    """Test successful summarization"""
    response = client.post(
        "/summarize/",  # Endpoint yo'lini tekshiring
        json={"text": "This is a long text that needs to be summarized."}
    )
    assert response.status_code == 200
    assert "summary" in response.json()
    assert response.json()["summary"] == "This is a mocked summary."
    mock_summarizer.assert_called_once()

def test_summarize_empty_text(client):
    """Test summarization with empty text"""
    response = client.post(
        "/summarize/",  # Endpoint yo'lini tekshiring
        json={"text": ""}
    )
    assert response.status_code == 422  # Validation error

