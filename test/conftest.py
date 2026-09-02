# tests/conftest.py
import pytest
import database


# Fixture for creating a temporary database for testing
@pytest.fixture
def test_db(tmp_path):
    database.DB_NAME = str(tmp_path / "test.db")
    database.init_database()
    return database
