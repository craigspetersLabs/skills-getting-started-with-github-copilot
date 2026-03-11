"""Tests for GET /activities endpoint"""


def test_get_activities_returns_all_activities(test_app):
    """Test that GET /activities returns all activities
    
    Arrange: Test client is ready with clean activities
    Act: Send GET request to /activities
    Assert: Response is 200 and contains all activities
    """
    # Arrange
    # (test_app fixture and clean_activities are set up by conftest)
    
    # Act
    response = test_app.get("/activities")
    data = response.json()
    
    # Assert
    assert response.status_code == 200
    assert len(data) > 0
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_get_activities_returns_correct_structure(test_app):
    """Test that activity objects have required fields
    
    Arrange: Test client is ready with clean activities
    Act: Send GET request to /activities
    Assert: Each activity has description, schedule, max_participants, participants
    """
    # Arrange
    # (test_app fixture and clean_activities are set up by conftest)
    
    # Act
    response = test_app.get("/activities")
    data = response.json()
    
    # Assert
    assert response.status_code == 200
    activity = data["Chess Club"]
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity
    assert isinstance(activity["participants"], list)
