#!/usr/bin/env python3

import sys
import os
import time

# Add the CARLA Python API to the path
carla_path = '/home/karthik.pakala@torc.ai/carla/PythonAPI/carla'
sys.path.append(carla_path)

try:
    import carla
    print("CARLA module imported successfully")
    
    # Try to connect to the CARLA server
    client = carla.Client('localhost', 2000)
    client.set_timeout(120.0)  # Increase timeout for large map loading
    
    # Test connection
    world = client.get_world()
    print(f"Successfully connected to CARLA server!")
    print(f"Current map: {world.get_map().name}")
    
    # Now let's load the converted OSM map
    print("Loading OSM-converted OpenDRIVE map...")
    
    # Read the converted XODR file
    xodr_path = os.path.expanduser("~/Downloads/semantic-62077.xodr")
    with open(xodr_path, 'r') as f:
        xodr_data = f.read()
    
    print(f"Loaded XODR file: {len(xodr_data)} characters")
    
    # Generate the OpenDRIVE world
    world = client.generate_opendrive_world(
        xodr_data, 
        carla.OpendriveGenerationParameters(
            vertex_distance=2.0,
            max_road_length=500.0,
            wall_height=1.0,
            additional_width=0.6,
            smooth_junctions=True,
            enable_mesh_visibility=True
        )
    )
    
    print("Successfully loaded the OSM map into CARLA!")
    print(f"New map: {world.get_map().name}")
    
    # Get some basic info about the map
    spawn_points = world.get_map().get_spawn_points()
    print(f"Number of available spawn points: {len(spawn_points)}")
    
    # Spawn a vehicle for testing
    blueprint_library = world.get_blueprint_library()
    vehicle_bp = blueprint_library.filter('vehicle')[0]  # Get the first available vehicle
    
    if spawn_points:
        spawn_point = spawn_points[0]
        vehicle = world.spawn_actor(vehicle_bp, spawn_point)
        print(f"Spawned vehicle: {vehicle.type_id} at {spawn_point.location}")
        
        # Let it run for a bit
        time.sleep(5)
        
        # Clean up
        vehicle.destroy()
        print("Vehicle destroyed")
    
    print("Simulation completed successfully!")
    
except ImportError as e:
    print(f"Error importing CARLA: {e}")
    print("Make sure CARLA Python API is properly installed")
except Exception as e:
    print(f"Error connecting to CARLA or running simulation: {e}")
    print("Make sure CARLA server is running on localhost:2000")