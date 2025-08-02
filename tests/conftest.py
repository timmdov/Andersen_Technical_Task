# tests/conftest.py
"""
Pytest configuration and fixtures for testing
"""

import sys
import os
import pytest

# Add the parent directory to Python path so tests can import from app/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


# Configure pytest
def pytest_configure(config):
    """Configure pytest settings"""
    print("🔧 Configuring pytest for User model tests...")


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Setup test environment"""
    print("🚀 Setting up test environment...")

    # This runs once before all tests
    yield

    # This runs once after all tests
    print("🧹 Cleaning up test environment...")


@pytest.fixture
def sample_user_data():
    """Fixture providing sample user data for tests"""
    return {
        'first_name': 'John',
        'last_name': 'Doe',
        'username': 'johndoe',
        'hashed_password': 'hashed_password_123'
    }


@pytest.fixture
def sample_user_data_minimal():
    """Fixture providing minimal user data (only required fields)"""
    return {
        'first_name': 'Jane',
        'username': 'janedoe',
        'hashed_password': 'hashed_password_456'
        # Note: last_name is optional, so not included
    }