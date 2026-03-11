"""Tests for POST /activities/{activity_name}/signup endpoint"""


def test_signup_for_activity_success(test_app):
    """Test successful signup for an activity
    
    Arrange: Test client ready, prepare test email
    Act: POST to /activities/Chess Club/signup?email=newstudent@mergington.edu
    Assert: Status 200, response contains success message, participant added
    """
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    
    # Act
    response = test_app.post(
        f"/activities/{activity_name}/signup?email={email}",
        params={"email": email}
    )
    data = response.json()
    
    # Assert
    assert response.status_code == 200
    assert "Signed up" in data["message"]
    assert email in data["message"]


def test_signup_participant_count_increases(test_app):
    """Test that participant count increases after signup
    
    Arrange: Get initial participant count for Chess Club
    Act: Sign up new participant
    Assert: Participant count increases by 1, email added to list
    """
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    
    initial_activities = test_app.get("/activities").json()
    initial_count = len(initial_activities[activity_name]["participants"])
    
    # Act
    test_app.post(
        f"/activities/{activity_name}/signup?email={email}",
        params={"email": email}
    )
    
    updated_activities = test_app.get("/activities").json()
    updated_count = len(updated_activities[activity_name]["participants"])
    
    # Assert
    assert updated_count == initial_count + 1
    assert email in updated_activities[activity_name]["participants"]


def test_signup_activity_not_found(test_app):
    """Test signup for non-existent activity
    
    Arrange: Prepare non-existent activity name
    Act: POST to /activities/NonExistent/signup
    Assert: Status 404, error detail message
    """
    # Arrange
    activity_name = "NonExistent"
    email = "newstudent@mergington.edu"
    
    # Act
    response = test_app.post(
        f"/activities/{activity_name}/signup?email={email}",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_email(test_app):
    """Test signup with duplicate email (student already signed up)
    
    Arrange: Chess Club already has michael@mergington.edu
    Act: Try to sign up michael@mergington.edu again
    Assert: Status 400, error detail message, participant count unchanged
    """
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already in Chess Club
    
    initial_activities = test_app.get("/activities").json()
    initial_count = len(initial_activities[activity_name]["participants"])
    
    # Act
    response = test_app.post(
        f"/activities/{activity_name}/signup?email={email}",
        params={"email": email}
    )
    
    updated_activities = test_app.get("/activities").json()
    updated_count = len(updated_activities[activity_name]["participants"])
    
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"
    assert updated_count == initial_count


def test_signup_activity_full(test_app):
    """Test signup when activity is at max capacity
    
    Arrange: Get an activity, fill it to max_participants
    Act: Try to sign up one more participant
    Assert: Status 400, activity full message, count unchanged
    """
    # Arrange
    # Find an activity with small max_participants
    activities_data = test_app.get("/activities").json()
    
    # Use Debate Team (max 14) and fill it
    activity_name = "Debate Team"
    activity = activities_data[activity_name]
    max_participants = activity["max_participants"]
    current_count = len(activity["participants"])
    
    # Add participants to reach max
    participants_needed = max_participants - current_count
    for i in range(participants_needed):
        email = f"student{i}@mergington.edu"
        test_app.post(
            f"/activities/{activity_name}/signup?email={email}",
            params={"email": email}
        )
    
    # Verify we're at max
    updated_activities = test_app.get("/activities").json()
    assert len(updated_activities[activity_name]["participants"]) == max_participants
    pre_full_count = len(updated_activities[activity_name]["participants"])
    
    # Act - Try to add one more
    overflow_email = "overflow@mergington.edu"
    response = test_app.post(
        f"/activities/{activity_name}/signup?email={overflow_email}",
        params={"email": overflow_email}
    )
    
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"
    
    final_activities = test_app.get("/activities").json()
    assert len(final_activities[activity_name]["participants"]) == pre_full_count


def test_signup_to_max_capacity(test_app):
    """Test successful signup exactly at max_participants
    
    Arrange: Fill activity to max_participants - 1
    Act: Sign up one more participant to reach exactly max
    Assert: Status 200, count equals max_participants
    """
    # Arrange
    activity_name = "Debate Team"
    activities_data = test_app.get("/activities").json()
    activity = activities_data[activity_name]
    max_participants = activity["max_participants"]
    current_count = len(activity["participants"])
    
    # Fill to max - 1
    participants_needed = max_participants - current_count - 1
    for i in range(participants_needed):
        email = f"filler{i}@mergington.edu"
        test_app.post(
            f"/activities/{activity_name}/signup?email={email}",
            params={"email": email}
        )
    
    # Act - Sign up to reach exactly max
    final_email = "finalseat@mergington.edu"
    response = test_app.post(
        f"/activities/{activity_name}/signup?email={final_email}",
        params={"email": final_email}
    )
    
    # Assert
    assert response.status_code == 200
    updated_activities = test_app.get("/activities").json()
    assert len(updated_activities[activity_name]["participants"]) == max_participants
    assert final_email in updated_activities[activity_name]["participants"]
