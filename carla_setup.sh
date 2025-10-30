#!/bin/bash

# CARLA Setup and Run Script
# This script helps you easily start CARLA server and run scenarios

CARLA_ROOT="/home/karthik.pakala@torc.ai/carla"
CARLA_DIST="/home/karthik.pakala@torc.ai/carla/Dist/CARLA_Shipping_da5fdfff0/LinuxNoEditor"
PYTHON_PATH="/home/karthik.pakala@torc.ai/carla/.venv/bin/python"

echo "🎮 CARLA Quick Setup"
echo "===================="

# Function to check if CARLA server is running
check_server() {
    $PYTHON_PATH -c "
import carla
try:
    client = carla.Client('localhost', 2000)
    client.set_timeout(2.0)
    world = client.get_world()
    print('✓ CARLA server is running')
    print('✓ Map:', world.get_map().name)
    exit(0)
except:
    print('❌ CARLA server is not running')
    exit(1)
" 2>/dev/null
}

# Function to start CARLA server
start_server() {
    echo "🚀 Starting CARLA server..."
    cd "$CARLA_DIST"
    nohup ./CarlaUE4.sh -nullrhi > carla_server.log 2>&1 &
    SERVER_PID=$!
    echo "✓ CARLA server started (PID: $SERVER_PID)"
    echo "⏳ Waiting 15 seconds for server to initialize..."
    sleep 15
}

# Function to stop CARLA server
stop_server() {
    echo "🛑 Stopping CARLA server..."
    pkill -f CarlaUE4
    echo "✓ CARLA server stopped"
}

# Main menu
case "$1" in
    "start")
        echo "Starting CARLA server..."
        start_server
        check_server
        ;;
    "stop")
        stop_server
        ;;
    "status")
        check_server
        ;;
    "run")
        # Check if server is running
        if ! check_server; then
            echo "Starting server first..."
            start_server
        fi
        
        # Run scenario launcher
        echo ""
        echo "🎯 Launching scenario menu..."
        cd "$CARLA_ROOT"
        $PYTHON_PATH scenario_launcher.py
        ;;
    "basic")
        if ! check_server; then
            echo "Starting server first..."
            start_server
        fi
        echo "🚗 Running basic scenario..."
        cd "$CARLA_ROOT"
        $PYTHON_PATH basic_scenario.py
        ;;
    "traffic")
        if ! check_server; then
            echo "Starting server first..."
            start_server
        fi
        echo "🚦 Running traffic scenario..."
        cd "$CARLA_ROOT"
        $PYTHON_PATH traffic_scenario.py
        ;;
    "sensor")
        if ! check_server; then
            echo "Starting server first..."
            start_server
        fi
        echo "📸 Running sensor scenario..."
        cd "$CARLA_ROOT"
        $PYTHON_PATH sensor_scenario.py
        ;;
    *)
        echo "Usage: $0 {start|stop|status|run|basic|traffic|sensor}"
        echo ""
        echo "Commands:"
        echo "  start   - Start CARLA server"
        echo "  stop    - Stop CARLA server"
        echo "  status  - Check if server is running"
        echo "  run     - Launch interactive scenario menu"
        echo "  basic   - Run basic vehicle scenario"
        echo "  traffic - Run traffic generation scenario"
        echo "  sensor  - Run sensor data collection scenario"
        echo ""
        echo "Examples:"
        echo "  $0 start    # Start the server"
        echo "  $0 basic    # Run basic scenario (starts server if needed)"
        echo "  $0 run      # Interactive menu"
        ;;
esac