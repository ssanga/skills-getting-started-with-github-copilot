"""Test configuration and fixtures for FastAPI application."""

import pytest
from fastapi.testclient import TestClient
from copy import deepcopy
from src.app import app
import src.app as app_module


@pytest.fixture
def test_activities():
    """Provide isolated test activities data for each test."""
    return {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": []
        }
    }


@pytest.fixture
def client(test_activities):
    """Provide a TestClient with isolated activities data."""
    # Store original activities
    original_activities = deepcopy(app_module.activities)
    
    # Replace with test activities
    app_module.activities = test_activities
    
    # Create test client
    test_client = TestClient(app)
    
    yield test_client
    
    # Restore original activities after test
    app_module.activities = original_activities
