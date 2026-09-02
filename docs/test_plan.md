# Test Plan — Embedded Event Simulator

## Overview
Checks that events get saved correctly and show up right in the CLI,
all without needing a real Arduino plugged in.

## Environment
- Python, Pytest, SQLite, GitHub Actions
- The serial connection is faked (mocked), so no real hardware is needed to run the tests

## Scope
| ID | Area | What It Tests |
|---|---|---|
| TC-001 | Database | Adding, looking up, and counting events works |
| TC-002 | Database | Timestamp and severity get saved correctly |
| TC-003 | Database | Bad input or an empty database doesn't crash anything |
| TC-004 | Serial | Good and bad messages get parsed correctly |
| TC-005 | Serial | Every event type maps to the right severity level |
| TC-006 | CLI | The events, summary, search, and system-failure commands show the right output |
| TC-007 | CLI | Empty results and bad search input are handled without crashing |

## Known Limitations
- Actual behavior on real hardware is checked manually, not by these automated tests
