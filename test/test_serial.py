import pytest
from unittest.mock import MagicMock
import serial_listener
import database
from datetime import datetime


# Fixture for creating a temporary database for testing
@pytest.fixture
def test_db(tmp_path):
    database.DB_NAME = str(tmp_path / "test.db")
    database.init_database()
    return database


# Test reading serial data
def test_read_serial_data():
    serial_listener.ser = MagicMock()
    serial_listener.ser.readline.return_value = b"TEMP_HIGH"
    result = serial_listener.read_serial_data()
    assert result == "TEMP_HIGH"


# Test read serial data none
def test_read_serial_data_invalid():
    serial_listener.ser = MagicMock()
    serial_listener.ser.readline.return_value = None
    result = serial_listener.read_serial_data()
    assert result == ""


# Test the process_serial_data function valid events
def test_process_serial_data_valid():
    assert serial_listener.process_serial_data("TEMP_HIGH") == True


# Test the process_serial_data function invalid events
def test_process_serial_data_invalid():
    assert serial_listener.process_serial_data("INVALID_EVENT") == False


# Test processing serial data empty
def test_process_serial_data_empty():
    assert serial_listener.process_serial_data("") == False


# Test writing to the database valid
def test_write_to_database(test_db):
    # Test writing to the database
    serial_listener.write_to_database("TEMP_HIGH", timestamp="2026-06-14 17:45:32")
    assert database.get_events() is not None
    assert database.get_events()[0][1] == "TEMP_HIGH"
    assert database.get_events()[0][2] == "2026-06-14 17:45:32"
    assert database.get_events()[0][3] == "MEDIUM"
    assert database.get_events()[0][4] is None
