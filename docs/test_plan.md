# Test Plan — Embedded Event Simulator

## Overview
Validates event ingestion, fault logging, and CLI
reporting without physical hardware.

## Environment
- Python, Pytest, SQLite, GitHub Actions
- Serial hardware simulated via MagicMock

## Scope
| ID | Area | What It Tests |
|---|---|---|
| TC-001 | Database | Event inserts, queries, and counts |
| TC-002 | Database | Timestamp and severity fields save correctly |
| TC-003 | Database | Invalid input and empty DB handled gracefully |
| TC-004 | Serial | Valid and invalid messages parsed correctly |
| TC-005 | Serial | All valid event types mapped to correct severity |
| TC-006 | CLI | Events, summary, search, and system-failure commands return correct output |
| TC-007 | CLI | Empty results and invalid search input handled gracefully |

## Out of Scope
- Duration tracking (deferred to V2)
- Live Arduino serial connection (mocked in CI)

## Known Limitations
- 30 tests total across 3 test files
- Physical hardware not required to run suite
