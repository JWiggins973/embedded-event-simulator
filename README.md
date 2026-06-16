# Embedded Event Simulator & Fault Monitor

[![Run Tests](https://github.com/JWiggins973/embedded-event-simulator/actions/workflows/python-app.yml/badge.svg)](https://github.com/JWiggins973/embedded-event-simulator/actions/workflows/python-app.yml)

---

## Purpose

Built a reusable embedded event simulation system using Arduino and Python to inject and process hardware-like signals, enabling deterministic testing of monitoring, logging, and alerting software behavior through an automated Pytest validation framework with mocked serial interfaces and a GitHub Actions CI pipeline.

---

## ⚙️ How It Works

1. The system simulates environmental hazards — high temperature, poor air quality, system fault, high humidity, and full system failure
2. Each hazard is triggered by a physical button press on the Arduino
3. Every button maps to a specific event type and is logged in real time to a SQLite database
4. When one hazard is active a red LED lights up and a single beep sounds. If all four are active simultaneously the buzzer runs continuously and the LED flashes until the hazard is cleared
5. From the command line a user can query all logged events using custom built CLI commands

### Button to Event Mapping

| Button | Event | Severity |
|---|---|---|
| Button 1 | TEMP_HIGH | MEDIUM |
| Button 2 | HUMIDITY_HIGH | MEDIUM |
| Button 3 | AIR_QUALITY_ALERT | HIGH |
| Button 4 | SYSTEM_FAULT | HIGH |
| All 4 | SYSTEM_FAILURE_CHECK_ALL | CRITICAL |

---

## 📁 Project Structure

```
embedded-event-simulator/
├── .github/
│   └── workflows/
│       └── tests.yml
├── arduino/
│   └── event_simulator.ino
├── backend/
│   ├── database.py
│   ├── serial_listener.py
│   └── cli.py
├── test/
│   ├── test_database.py
│   ├── test_serial.py
│   └── test_cli.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🛠 Stack

| Layer | Technology |
|---|---|
| Firmware | Arduino UNO, C++ |
| Serial Processing | Python, pyserial |
| Database | SQLite |
| CLI | Click |
| Testing | Pytest, unittest.mock |
| CI/CD | GitHub Actions |

---

## 💻 Run Locally

```bash
git clone https://github.com/JWiggins973/embedded-event-simulator.git
cd embedded-event-simulator
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Connect your Arduino and start the serial listener:

```bash
python backend/serial_listener.py
```

---

## ⌨️ CLI Commands

```bash
python backend/cli.py events              # show all logged events
python backend/cli.py summary             # show event counts by type
python backend/cli.py search TEMP_HIGH    # search for a specific event type
python backend/cli.py system-failure      # show system failure events only
```

All events display with timestamp, severity level, and duration. Duration shows `None` in V1 — recovery event tracking coming in V2.

---

## 🗄 Database Schema

```sql
CREATE TABLE IF NOT EXISTS Events (
    id          INTEGER PRIMARY KEY,
    event_type  TEXT,
    timestamp   DATETIME,
    severity    TEXT,
    duration    INTEGER
);
```

---

## 🧪 Testing

30 tests covering core functionality and edge cases including mocked hardware interfaces. Tests run without Arduino connected.

```bash
pytest test/ -v
```

Tests run automatically on every push via GitHub Actions.

### Test Coverage

| File | Tests | Coverage |
|---|---|---|
| test_database.py | 11 | Insert, query, filter, aggregation, edge cases |
| test_serial.py | 8 | Validation, mocked serial, severity mapping |
| test_cli.py | 11 | All commands, formatting, empty states, edge cases |

---

## 📍 V2 Roadmap

- Swap Arduino for ESP32 with WiFi — serial replaced with HTTP POST
- FastAPI endpoint replaces serial listener
- PostgreSQL replaces SQLite
- Phone notifications via Discord webhook or ntfy.sh
- Tableau dashboard connects to PostgreSQL
- Click CLI remains, expanded with more commands

---

## 🔗 Hardware References

- [TinkerCAD Schematic](https://www.tinkercad.com/things/cTCtQ8Y2Rf1-embedded-event-simulator)
- [RexQualis Arduino UNO R3 Kit](https://www.amazon.com/REXQualis-Development-Membrane-Receiver-Detailed/dp/B074WMHLQ4)