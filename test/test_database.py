import pytest
import database


# Fixture for creating a temporary database for testing
@pytest.fixture
def test_db(tmp_path):
    database.DB_NAME = str(tmp_path / "test.db")
    database.init_database()
    return database


# Fixture for creating a populated database for testing
@pytest.fixture
def populated_db(test_db):
    test_db.insert_event("TEMP_HIGH", "2026-06-14 17:45:32", "MEDIUM", None)
    test_db.insert_event("SYSTEM_FAULT", "2026-06-14 17:46:00", "CRITICAL", None)
    test_db.insert_event("HUMIDITY_HIGH", "2026-06-14 17:47:00", "MEDIUM", None)
    return test_db


# Test the insertion of a new event
def test_insert_event(test_db):
    test_db.insert_event("TEMP_HIGH", "2026-06-14 17:45:32", "MEDIUM", None)
    assert test_db.get_events() == [
        (1, "TEMP_HIGH", "2026-06-14 17:45:32", "MEDIUM", None)
    ]


# Test inserting multiple events
def test_insert_events_many(test_db):
    events = [
        ("TEMP_HIGH", "2026-06-14 17:45:32", "MEDIUM", None),
        ("SYSTEM_FAULT", "2026-06-14 17:46:00", "CRITICAL", None),
        ("HUMIDITY_HIGH", "2026-06-14 17:47:00", "MEDIUM", None),
    ]
    for event in events:
        test_db.insert_event(*event)
    assert test_db.get_events() == [
        (1, "TEMP_HIGH", "2026-06-14 17:45:32", "MEDIUM", None),
        (2, "SYSTEM_FAULT", "2026-06-14 17:46:00", "CRITICAL", None),
        (3, "HUMIDITY_HIGH", "2026-06-14 17:47:00", "MEDIUM", None),
    ]


# Test inserting five events
def test_insert_five_events(test_db):
    events = [
        ("TEMP_HIGH", "2026-06-14 17:45:32", "MEDIUM", None),
        ("SYSTEM_FAULT", "2026-06-14 17:46:00", "CRITICAL", None),
        ("HUMIDITY_HIGH", "2026-06-14 17:47:00", "MEDIUM", None),
        ("SYSTEM_FAILURE_CHECK_ALL", "2026-06-14 17:48:00", "CRITICAL", None),
        ("TEMP_LOW", "2026-06-14 17:49:00", "MEDIUM", None),
    ]
    for event in events:
        test_db.insert_event(*event)
    assert len(test_db.get_events()) == 5


# Test that the database is empty
def test_empty_database(test_db):
    assert test_db.get_events() == []


# Test getting events by type
def test_get_event_by_type(populated_db):
    assert populated_db.get_events_by_type("TEMP_HIGH") == [
        (1, "TEMP_HIGH", "2026-06-14 17:45:32", "MEDIUM", None)
    ]
    assert populated_db.get_events_by_type("SYSTEM_FAULT") == [
        (2, "SYSTEM_FAULT", "2026-06-14 17:46:00", "CRITICAL", None)
    ]
    assert populated_db.get_events_by_type("HUMIDITY_HIGH") == [
        (3, "HUMIDITY_HIGH", "2026-06-14 17:47:00", "MEDIUM", None)
    ]


# Test getting all events
def test_get_events(populated_db):
    assert populated_db.get_events() == [
        (1, "TEMP_HIGH", "2026-06-14 17:45:32", "MEDIUM", None),
        (2, "SYSTEM_FAULT", "2026-06-14 17:46:00", "CRITICAL", None),
        (3, "HUMIDITY_HIGH", "2026-06-14 17:47:00", "MEDIUM", None),
    ]


# Test getting events by type not found
def test_get_events_by_type_not_found(populated_db):
    assert populated_db.get_events_by_type("NONEXISTENT") == []


# Test getting the summary of events
def test_get_summary(populated_db):
    summary = populated_db.get_summary()
    assert summary == [("HUMIDITY_HIGH", 1), ("SYSTEM_FAULT", 1), ("TEMP_HIGH", 1)]


# Test count of events in summary
def test_summary_count(populated_db):
    populated_db.insert_event("TEMP_HIGH", "2026-06-14 17:48:00", "MEDIUM", None)
    summary = populated_db.get_summary()
    assert len(summary) == 3
    assert summary == [("HUMIDITY_HIGH", 1), ("SYSTEM_FAULT", 1), ("TEMP_HIGH", 2)]


# Test summary when no events are found
def test_get_summary_not_found(test_db):
    summary = test_db.get_summary()
    assert summary == []
