"""Pytest configuration and fixtures for FastAPI app tests"""

import pytest
import copy
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def test_app():
    """Provide a TestClient instance for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def clean_activities():
    """Provide a fresh deep copy of activities for each test"""
    return copy.deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities(clean_activities):
    """Reset activities dict to clean state before each test (autouse)"""
    activities.clear()
    activities.update(clean_activities)
    yield
    # Cleanup after test
    activities.clear()
    activities.update(clean_activities)
