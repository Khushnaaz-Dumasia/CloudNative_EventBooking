#!/bin/bash
source venv/bin/activate


# to run this file
# 1. chmod +x run_all.sh
# 2. ./run_all.sh

# Run this script from the root directory
# Kill any old versions first
pkill -f uvicorn
pkill -f "http.server"
# More aggressive port-based cleanup
lsof -ti :8080,8001,8002,8003 | xargs kill -9 2>/dev/null
sleep 1 # Give them a moment to release ports

echo "Starting Services..."

export PYTHONPATH=$(pwd)/user_service
uvicorn main:app --app-dir user_service --port 8001 > user.log 2>&1 &

export PYTHONPATH=$(pwd)/event_service
uvicorn main:app --app-dir event_service --port 8002 > event.log 2>&1 &

export PYTHONPATH=$(pwd)/booking_service
uvicorn main:app --app-dir booking_service --port 8003 > booking.log 2>&1 &

sleep 3 # Give them a moment to start

echo "Starting Frontend on 8080..."
cd frontend && python3 -m http.server 8080