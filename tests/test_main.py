def test_docs_available(client):
    """Test that API documentation is available"""
    response = client.get("/docs")
    assert response.status_code == 200
    assert "swagger" in response.text.lower()