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


"""Test the events command"""


# Test the events command with no data
def test_events_command(test_db):
    runner = CliRunner()
    result = runner.invoke(cli, ["events"])
    assert result.exit_code == 0
    assert result.output == ""


# Test the events command with data
def test_events_command_with_data(populated_db):
    runner = CliRunner()
    result = runner.invoke(cli, ["events"])
    assert result.exit_code == 0
    assert "EVENT: TEMP_HIGH" in result.output
    assert "EVENT: SYSTEM_FAULT" in result.output
    assert "EVENT: HUMIDITY_HIGH" in result.output
    assert "EVENT: SYSTEM_FAILURE_CHECK_ALL" in result.output


# Test the events command output
def test_events_command_output(populated_db):
    runner = CliRunner()
    result = runner.invoke(cli, ["events"])
    assert result.exit_code == 0
    assert "EVENT: TEMP_HIGH" in result.output
    assert "EVENT: SYSTEM_FAULT" in result.output
    assert "EVENT: HUMIDITY_HIGH" in result.output
    assert "EVENT: SYSTEM_FAILURE_CHECK_ALL" in result.output


# Test the formatting of the events command
def test_events_command_formating(populated_db):
    runner = CliRunner()
    result = runner.invoke(cli, ["events"])
    assert result.exit_code == 0
    assert (
        "EVENT: TEMP_HIGH | TIME: 2026-06-14 17:45:32 | SEVERITY: MEDIUM"
        in result.output
    )
    assert (
        "EVENT: SYSTEM_FAULT | TIME: 2026-06-14 17:46:00 | SEVERITY: CRITICAL"
        in result.output
    )
    assert (
        "EVENT: HUMIDITY_HIGH | TIME: 2026-06-14 17:47:00 | SEVERITY: MEDIUM"
        in result.output
    )
    assert (
        "EVENT: SYSTEM_FAILURE_CHECK_ALL | TIME: 2026-06-14 17:48:00 | SEVERITY: CRITICAL"
        in result.output
    )


"""Test the summary command"""


# Test the summary command with no data
def test_summary_command(test_db):
    runner = CliRunner()
    result = runner.invoke(cli, ["summary"])
    assert result.exit_code == 0
    assert "No events found" in result.output


# Test the summary command with data
def test_summary_command_with_data(populated_db):
    runner = CliRunner()
    result = runner.invoke(cli, ["summary"])
    assert result.exit_code == 0
    assert "EVENT: TEMP_HIGH | COUNT: 1" in result.output
    assert "EVENT: SYSTEM_FAULT | COUNT: 1" in result.output
    assert "EVENT: HUMIDITY_HIGH | COUNT: 1" in result.output
    assert "EVENT: SYSTEM_FAILURE_CHECK_ALL | COUNT: 1" in result.output


"""Test the search command"""


# Test the search command with no data
def test_search_command(test_db):
    runner = CliRunner()
    result = runner.invoke(cli, ["search", "TEMP_HIGH"])
    assert result.exit_code == 0
    assert "EVENT: TEMP_HIGH" not in result.output


# Test the search command with invalid input
def test_search_command_invalid_input(test_db):
    runner = CliRunner()
    result = runner.invoke(cli, ["search", "INVALID_EVENT"])
    assert result.exit_code == 0
    assert "EVENT: INVALID_EVENT" not in result.output
    assert "No events found for type: INVALID_EVENT" in result.output


# Test the search command with data
def test_search_command_with_data(populated_db):
    runner = CliRunner()
    result = runner.invoke(cli, ["search", "TEMP_HIGH"])
    assert result.exit_code == 0
    assert "EVENT: TEMP_HIGH" in result.output


# Test the formatting of the search command
def test_search_command_formatting(populated_db):
    runner = CliRunner()
    result = runner.invoke(cli, ["search", "TEMP_HIGH"])
    assert result.exit_code == 0
    assert (
        "EVENT: TEMP_HIGH | TIME: 2026-06-14 17:45:32 | SEVERITY: MEDIUM"
        in result.output
    )


"""Test the system failures command"""


# Test the system failures command with no data
def test_system_failures_command(test_db):
    runner = CliRunner()
    result = runner.invoke(cli, ["system-failure"])
    assert result.exit_code == 0
    assert "No system failures found" in result.output
    assert "EVENT: SYSTEM_FAILURE_CHECK_ALL" not in result.output


# Test the system failures command with data
def test_system_failures_command_with_data(populated_db):
    runner = CliRunner()
    result = runner.invoke(cli, ["system-failure"])
    assert result.exit_code == 0
    assert "No system failures found" not in result.output
    assert "EVENT: SYSTEM_FAILURE_CHECK_ALL" in result.output


# Test the formatting of the system failures command
def test_system_failures_command_formatting(populated_db):
    runner = CliRunner()
    result = runner.invoke(cli, ["system-failure"])
    assert result.exit_code == 0
    assert (
        "EVENT: SYSTEM_FAILURE_CHECK_ALL | TIME: 2026-06-14 17:48:00 | SEVERITY: CRITICAL"
        in result.output
    )
