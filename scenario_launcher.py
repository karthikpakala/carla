#!/usr/bin/env python3

"""
CARLA Scenario Launcher
Easy way to run different CARLA scenarios
"""

import subprocess
import sys
import os
import time

def check_server():
    """Check if CARLA server is running"""
    try:
        import carla
        client = carla.Client('localhost', 2000)
        client.set_timeout(2.0)
        world = client.get_world()
        return True, world.get_map().name
    except:
        return False, None

def start_server():
    """Instructions to start CARLA server"""
    print("🚨 CARLA server is not running!")
    print("\nTo start the server, run this command in another terminal:")
    print('cd "/home/karthik.pakala@torc.ai/carla/Dist/CARLA_Shipping_da5fdfff0/LinuxNoEditor/"')
    print("nohup ./CarlaUE4.sh -nullrhi > carla_server.log 2>&1 &")
    print("\nThen wait about 10 seconds for it to start, and try again.")

def main():
    print("🎮 CARLA Scenario Launcher")
    print("=" * 50)
    
    # Check if server is running
    server_running, map_name = check_server()
    if not server_running:
        start_server()
        return 1
    
    print(f"✓ CARLA server is running (Map: {map_name})")
    
    # Available scenarios
    scenarios = {
        '1': ('Basic Vehicle', 'basic_scenario.py', 'Simple vehicle with autopilot'),
        '2': ('Traffic Generation', 'traffic_scenario.py', 'Multiple vehicles creating traffic'),
        '3': ('Sensor Data Collection', 'sensor_scenario.py', 'Vehicle with cameras and LiDAR'),
        '4': ('Official Tutorial', 'PythonAPI/examples/tutorial.py', 'CARLA official tutorial'),
        '5': ('Generate Traffic', 'PythonAPI/examples/generate_traffic.py', 'Official traffic generator'),
        '6': ('Manual Control', 'PythonAPI/examples/manual_control.py', 'Drive manually with pygame'),
        '7': ('Dynamic Weather', 'PythonAPI/examples/dynamic_weather.py', 'Weather effects demo'),
        '8': ('Synchronous Mode', 'PythonAPI/examples/synchronous_mode.py', 'Synchronous simulation'),
    }
    
    print(f"\n📋 Available Scenarios:")
    print("-" * 50)
    for key, (name, script, desc) in scenarios.items():
        print(f"{key}. {name}")
        print(f"   📄 {script}")
        print(f"   📝 {desc}")
        print()
    
    # Get user choice
    while True:
        choice = input("Enter scenario number (1-8) or 'q' to quit: ").strip()
        
        if choice.lower() == 'q':
            print("👋 Goodbye!")
            return 0
        
        if choice in scenarios:
            name, script_path, desc = scenarios[choice]
            break
        else:
            print("❌ Invalid choice. Please enter 1-8 or 'q'")
    
    # Run the chosen scenario
    print(f"\n🚀 Running: {name}")
    print(f"📄 Script: {script_path}")
    print(f"📝 Description: {desc}")
    print("-" * 50)
    
    # Build command
    python_path = "/home/karthik.pakala@torc.ai/carla/.venv/bin/python"
    full_script_path = f"/home/karthik.pakala@torc.ai/carla/{script_path}"
    
    if not os.path.exists(full_script_path):
        print(f"❌ Script not found: {full_script_path}")
        return 1
    
    try:
        # Run the scenario
        result = subprocess.run([python_path, full_script_path], 
                              cwd="/home/karthik.pakala@torc.ai/carla/")
        
        if result.returncode == 0:
            print(f"\n✅ Scenario '{name}' completed successfully!")
        else:
            print(f"\n⚠️  Scenario '{name}' exited with code {result.returncode}")
            
    except KeyboardInterrupt:
        print(f"\n⏹️  Scenario '{name}' interrupted by user")
    except Exception as e:
        print(f"\n❌ Error running scenario: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())