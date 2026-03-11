"""Tests for root endpoint"""

def test_root_redirects_to_static_index(test_app):
    """Test that GET / redirects to /static/index.html
    
    Arrange: Test client is ready
    Act: Send GET request to /
    Assert: Response is 307 redirect to /static/index.html
    """
    # Arrange
    # (test_app fixture provides the TestClient)
    
    # Act
    response = test_app.get("/", follow_redirects=False)
    
    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"
