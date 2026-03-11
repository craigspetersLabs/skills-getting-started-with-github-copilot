"""Tests for DELETE /activities/{activity_name}/unregister endpoint"""


def test_unregister_from_activity_success(test_app):
    """Test successful unregister from an activity
    
    Arrange: Chess Club has michael@mergington.edu
    Act: DELETE /activities/Chess Club/unregister?email=michael@mergington.edu
    Assert: Status 200, success message returned
    """
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already in Chess Club
    
    # Verify participant exists
    activities_data = test_app.get("/activities").json()
    assert email in activities_data[activity_name]["participants"]
    
    # Act
    response = test_app.delete(
        f"/activities/{activity_name}/unregister?email={email}",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]
    assert email in response.json()["message"]


def test_unregister_participant_count_decreases(test_app):
    """Test that participant count decreases after unregister
    
    Arrange: Get initial participant count for Chess Club
    Act: Unregister michael@mergington.edu
    Assert: Participant count decreases by 1, email removed from list
    """
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    
    initial_activities = test_app.get("/activities").json()
    initial_count = len(initial_activities[activity_name]["participants"])
    
    # Act
    test_app.delete(
        f"/activities/{activity_name}/unregister?email={email}",
        params={"email": email}
    )
    
    updated_activities = test_app.get("/activities").json()
    updated_count = len(updated_activities[activity_name]["participants"])
    
    # Assert
    assert updated_count == initial_count - 1
    assert email not in updated_activities[activity_name]["participants"]


def test_unregister_activity_not_found(test_app):
    """Test unregister from non-existent activity
    
    Arrange: Prepare non-existent activity name
    Act: DELETE /activities/NonExistent/unregister
    Assert: Status 404, error detail message
    """
    # Arrange
    activity_name = "NonExistent"
    email = "someone@mergington.edu"
    
    # Act
    response = test_app.delete(
        f"/activities/{activity_name}/unregister?email={email}",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_participant_not_found(test_app):
    """Test unregister when participant is not in activity
    
    Arrange: Chess Club doesn't have notinlist@mergington.edu
    Act: Try to unregister notinlist@mergington.edu
    Assert: Status 404, participant not found message
    """
    # Arrange
    activity_name = "Chess Club"
    email = "notinlist@mergington.edu"
    
    # Verify participant doesn't exist
    activities_data = test_app.get("/activities").json()
    assert email not in activities_data[activity_name]["participants"]
    initial_count = len(activities_data[activity_name]["participants"])
    
    # Act
    response = test_app.delete(
        f"/activities/{activity_name}/unregister?email={email}",
        params={"email": email}
    )
    
    updated_activities = test_app.get("/activities").json()
    updated_count = len(updated_activities[activity_name]["participants"])
    
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
    assert updated_count == initial_count


def test_unregister_from_empty_activity(test_app):
    """Test unregister when activity has no participants
    
    Arrange: Sign up and unregister until activity is empty, then try to unregister again
    Act: Try to delete non-existent participant from empty activity
    Assert: Status 404, participant not found
    """
    # Arrange
    activity_name = "Drama Club"  # Start with anna@mergington.edu
    email = "anna@mergington.edu"
    
    # Get initial state
    activities_data = test_app.get("/activities").json()
    initial_participants = activities_data[activity_name]["participants"].copy()
    
    # Unregister the only participant (anna)
    test_app.delete(
        f"/activities/{activity_name}/unregister?email={email}",
        params={"email": email}
    )
    
    # Verify activity is now empty
    updated_activities = test_app.get("/activities").json()
    assert len(updated_activities[activity_name]["participants"]) == 0
    
    # Act - Try to unregister from empty activity
    response = test_app.delete(
        f"/activities/{activity_name}/unregister?email={email}",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
