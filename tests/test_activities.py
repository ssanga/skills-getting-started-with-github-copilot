"""Unit tests for FastAPI activities endpoints."""

import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint."""

    def test_get_activities_returns_all_activities(self, client):
        """Verify GET /activities returns all activities with correct structure."""
        response = client.get("/activities")
        
        assert response.status_code == 200
        data = response.json()
        
        # Check all test activities are returned
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Gym Class" in data
        
        # Verify structure of activity object
        chess = data["Chess Club"]
        assert "description" in chess
        assert "schedule" in chess
        assert "max_participants" in chess
        assert "participants" in chess
        assert isinstance(chess["participants"], list)


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint."""

    def test_signup_for_activity_success(self, client):
        """Verify successful signup adds participant to activity."""
        response = client.post(
            "/activities/Gym%20Class/signup?email=john@mergington.edu"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "john@mergington.edu" in data["message"]
        assert "Gym Class" in data["message"]
        
        # Verify participant was actually added
        activities = client.get("/activities").json()
        assert "john@mergington.edu" in activities["Gym Class"]["participants"]

    def test_signup_adds_participant_to_existing_list(self, client):
        """Verify signup adds participant to activity with existing participants."""
        response = client.post(
            "/activities/Chess%20Club/signup?email=sarah@mergington.edu"
        )
        
        assert response.status_code == 200
        
        # Verify participant was added without removing existing ones
        activities = client.get("/activities").json()
        chess_participants = activities["Chess Club"]["participants"]
        
        assert "michael@mergington.edu" in chess_participants
        assert "sarah@mergington.edu" in chess_participants
        assert len(chess_participants) == 2


class TestUnregisterFromActivity:
    """Tests for DELETE /activities/{activity_name}/signup endpoint."""

    def test_unregister_from_activity_success(self, client):
        """Verify successful unregister removes participant from activity."""
        response = client.delete(
            "/activities/Chess%20Club/signup?email=michael@mergington.edu"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "michael@mergington.edu" in data["message"]
        assert "Chess Club" in data["message"]
        
        # Verify participant was actually removed
        activities = client.get("/activities").json()
        assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]

    def test_unregister_maintains_other_participants(self, client):
        """Verify unregister removes only the specified participant."""
        # First add another participant to Chess Club
        client.post("/activities/Chess%20Club/signup?email=alex@mergington.edu")
        
        # Now unregister first participant
        response = client.delete(
            "/activities/Chess%20Club/signup?email=michael@mergington.edu"
        )
        
        assert response.status_code == 200
        
        # Verify only the removed participant is gone
        activities = client.get("/activities").json()
        chess_participants = activities["Chess Club"]["participants"]
        
        assert "michael@mergington.edu" not in chess_participants
        assert "alex@mergington.edu" in chess_participants


class TestRootRedirect:
    """Tests for GET / endpoint."""

    def test_root_redirect_to_index(self, client):
        """Verify root path redirects to static index page."""
        response = client.get("/", follow_redirects=False)
        
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"
