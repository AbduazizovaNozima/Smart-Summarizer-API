def test_read_root(client):
    """Test the root endpoint returns correct welcome message"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome to Smart Summarizer API" in response.text

def test_docs_available(client):
    """Test that API documentation is available"""
    response = client.get("/docs")
    assert response.status_code == 200
    assert "swagger" in response.text.lower()