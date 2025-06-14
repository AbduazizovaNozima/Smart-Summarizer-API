import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mock_summarizer():
    with patch('app.services.summarizer.SummarizerService.summarize') as mock:
        mock.return_value = "This is a mocked summary."
        yield mock