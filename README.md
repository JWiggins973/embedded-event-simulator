# Embedded Event Simulator & Fault Monitor

[![Run Tests](https://github.com/JWiggins973/embedded-event-simulator/actions/workflows/python-app.yml/badge.svg)](https://github.com/JWiggins973/embedded-event-simulator/actions/workflows/python-app.yml)

Hazard simulator with LED indicators and buzzer when system completely fails. Quality assurance with extensive Pytest suite and event logger.

## 🧪 Testing

30 tests covering core functionality and edge cases including mocked hardware interfaces. Runs without Arduino connected.

```bash
pytest test/ -v
```

| File | Tests | What's Covered |
|---|---|---|
| test_database.py | 10 | Insert, query, filter, counting, edge cases |
| test_serial.py | 7 | Validation, mocked serial, severity mapping |
| test_cli.py | 13 | All commands, formatting, empty states, edge cases |

## ⚙️ How It Works

1. Press a button to trigger a hazard event. Arduino sends it over serial to Python.
2. Python validates, assigns severity, and logs it to SQLite with a timestamp.
3. All 4 buttons pressed simultaneously triggers the buzzer and flashing LED until cleared.

### Button to Event Mapping

| Button | Event | Severity |
|---|---|---|
| Button 1 | TEMP_HIGH | MEDIUM |
| Button 2 | HUMIDITY_HIGH | MEDIUM |
| Button 3 | AIR_QUALITY_ALERT | HIGH |
| Button 4 | SYSTEM_FAULT | HIGH |
| All 4 | SYSTEM_FAILURE_CHECK_ALL | CRITICAL |

## 🛠 Stack

- **Firmware:** Arduino UNO, C++
- **Serial Processing:** Python, pyserial
- **Database:** SQLite
- **CLI:** Click
- **Testing:** Pytest, unittest.mock
- **CI/CD:** GitHub Actions

## 📁 Project Structure

```
embedded-event-simulator/
├── .github/workflows/tests.yml
├── arduino/event_simulator.ino
├── backend/
│   ├── database.py
│   ├── serial_listener.py
│   └── cli.py
├── test/
│   ├── test_database.py
│   ├── test_serial.py
│   └── test_cli.py
├── requirements.txt
└── README.md
```

## ⌨️ CLI Commands

```bash
python backend/cli.py events            # All logged events
python backend/cli.py summary           # Event counts by type
python backend/cli.py search TEMP_HIGH  # Search by event type
python backend/cli.py system-failure    # System failure events only
```

Duration shows `None` in V1. Recovery event tracking coming in V2.

## 💻 Run Locally

```bash
git clone https://github.com/JWiggins973/embedded-event-simulator.git
cd embedded-event-simulator
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python backend/serial_listener.py
```

## 📍 Coming Soon

ESP32 with WiFi support.

## 🔗 Hardware References

- [TinkerCAD Schematic](https://www.tinkercad.com/things/cTCtQ8Y2Rf1-embedded-event-simulator)
- [RexQualis Arduino UNO R3 Kit](https://www.amazon.com/REXQualis-Development-Membrane-Receiver-Detailed/dp/B074WMHLQ4)