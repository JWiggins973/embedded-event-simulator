import pytest
from click.testing import CliRunner
from cli import cli
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
    test_db.insert_event(
        "SYSTEM_FAILURE_CHECK_ALL", "2026-06-14 17:48:00", "CRITICAL", None
    )
    return test_db


def test_events_command(test_db):
    runner = CliRunner()
    result = runner.invoke(cli, ["events"])
    assert result.exit_code == 0
    assert result.output == ""


def test_events_command_with_data(populated_db):
    runner = CliRunner()
    result = runner.invoke(cli, ["events"])
    assert result.exit_code == 0
    assert "TEMP_HIGH" in result.output
    assert "SYSTEM_FAULT" in result.output
    assert "HUMIDITY_HIGH" in result.output


def test_summary_command(test_db):
    runner = CliRunner()
    result = runner.invoke(cli, ["summary"])
    assert result.exit_code == 0
    assert result.output == ""


def test_summary_command_with_data(populated_db):
    runner = CliRunner()
    result = runner.invoke(cli, ["summary"])
    assert result.exit_code == 0
    assert "('TEMP_HIGH', 1)" in result.output
    assert "('SYSTEM_FAULT', 1)" in result.output
    assert "('HUMIDITY_HIGH', 1)" in result.output
    assert "('SYSTEM_FAILURE_CHECK_ALL', 1)" in result.output


def test_search_command(test_db):
    runner = CliRunner()
    result = runner.invoke(cli, ["search", "TEMP_HIGH"])
    assert result.exit_code == 0
    assert "TEMP_HIGH" not in result.output


def test_search_command_with_data(populated_db):
    runner = CliRunner()
    result = runner.invoke(cli, ["search", "TEMP_HIGH"])
    assert result.exit_code == 0
    assert "TEMP_HIGH" in result.output


def test_system_failures_command(test_db):
    runner = CliRunner()
    result = runner.invoke(cli, ["system-failure"])
    assert result.exit_code == 0
    assert "SYSTEM_FAILURE_CHECK_ALL" not in result.output


def test_system_failures_command_with_data(populated_db):
    runner = CliRunner()
    result = runner.invoke(cli, ["system-failure"])
    assert result.exit_code == 0
    assert "SYSTEM_FAILURE_CHECK_ALL" in result.output
