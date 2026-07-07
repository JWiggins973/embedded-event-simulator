#!/bin/bash
cd "$(dirname "$0")"

source venv/bin/activate

if [ ! -f "venv/bin/activate" ]; then
    echo "Virtual environment not found. Please set up the virtual environment first."
    exit 1
fi

source venv/bin/activate

while true; do
    echo ""
    echo "Embedded Event Sim"
    echo "1) Start Listener"
    echo "2) View Events"
    echo "3) View Summary"
    echo "4) Search Events"
    echo "5) Run Tests"
    echo "6) Exit"
    echo ""
    read -p "Choose: " choice

    case $choice in
        1) python backend/serial_listener.py ;;
        2) python backend/cli.py events ;;
        3) python backend/cli.py summary ;;
        4) read -p "Event type: " event
           python backend/cli.py search "$event" ;;
        5) pytest test/ -v ;;
        6) exit 0 ;;
        *) echo "Invalid choice" ;;
    esac
done


