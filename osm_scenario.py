#!/usr/bin/env python

# Copyright (c) 2025 Computer Vision Center (CVC) at the Universitat Autonoma
# de Barcelona (UAB).
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

"""
OSM Map Scenario Runner

This script demonstrates how to:
1. Load an OSM map from a file
2. Convert it to OpenDRIVE format
3. Generate a CARLA world with the map
4. Spawn vehicles and run a simple scenario

Usage:
    python osm_scenario.py --osm-path /path/to/your/map.osm
"""

import glob
import os
import sys
import time
import random
import argparse

# CARLA Python API should be installed via pip
# If not installed, use: pip install PythonAPI/carla/dist/carla-*.whl

import carla

def load_osm_map(client, osm_file_path):
    """
    Load an OSM map file and convert it to a CARLA world
    
    Args:
        client: CARLA client instance
        osm_file_path: Path to the OSM file
    
    Returns:
        world: CARLA world with the loaded map
    """
    print(f"Loading OSM file: {osm_file_path}")
    
    if not os.path.exists(osm_file_path):
        raise FileNotFoundError(f"OSM file not found: {osm_file_path}")
    
    # Read the OSM file
    with open(osm_file_path, 'r', encoding='utf-8') as osm_file:
        osm_data = osm_file.read()
    
    print("Converting OSM data to OpenDRIVE format...")
    
    # Configure OSM to OpenDRIVE conversion settings
    settings = carla.Osm2OdrSettings()
    
    # Set which OSM way types to include in the conversion
    settings.set_osm_way_types([
        "motorway", "motorway_link",
        "trunk", "trunk_link", 
        "primary", "primary_link",
        "secondary", "secondary_link", 
        "tertiary", "tertiary_link",
        "unclassified", "residential",
        "service", "living_street"
    ])
    
    # Set traffic light excluded way types (ways that shouldn't have traffic lights)
    settings.set_tl_excluded_way_types([
        "motorway", "motorway_link",
        "trunk", "trunk_link",
        "service"
    ])
    
    # Configure other settings
    settings.use_offsets = True
    settings.default_lane_width = 3.5  # meters
    settings.elevation_layer_height = 0.0  # meters
    
    # Convert OSM to OpenDRIVE
    xodr_data = carla.Osm2Odr.convert(osm_data, settings)
    
    print("Generating CARLA world from OpenDRIVE data...")
    
    # Configure world generation parameters
    generation_params = carla.OpendriveGenerationParameters(
        vertex_distance=2.0,        # Distance between vertices in the mesh
        max_road_length=500.0,      # Maximum length of road segments
        wall_height=0.0,            # Height of walls along roads
        additional_width=0.6,       # Additional width for roads
        smooth_junctions=True,      # Smooth junction connections
        enable_mesh_visibility=True # Enable mesh visibility
    )
    
    # Generate the world
    world = client.generate_opendrive_world(xodr_data, generation_params)
    
    print("OSM map successfully loaded into CARLA!")
    return world

def spawn_ego_vehicle(world, blueprint_library):
    """
    Spawn the ego vehicle (main vehicle) at a random spawn point
    
    Args:
        world: CARLA world
        blueprint_library: CARLA blueprint library
    
    Returns:
        actor: Spawned vehicle actor
    """
    # Get vehicle blueprints
    vehicle_blueprints = blueprint_library.filter('vehicle.*')
    
    # Choose a random vehicle blueprint
    ego_bp = random.choice(vehicle_blueprints)
    
    # Try to set the color if available
    if ego_bp.has_attribute('color'):
        color = random.choice(ego_bp.get_attribute('color').recommended_values)
        ego_bp.set_attribute('color', color)
    
    # Get spawn points
    spawn_points = world.get_map().get_spawn_points()
    
    if not spawn_points:
        print("No spawn points available! The map might not have proper spawn locations.")
        return None
    
    # Try to spawn the vehicle at different spawn points
    for i in range(min(10, len(spawn_points))):
        spawn_point = random.choice(spawn_points)
        
        try:
            ego_vehicle = world.spawn_actor(ego_bp, spawn_point)
            print(f"Ego vehicle spawned at: {spawn_point.location}")
            return ego_vehicle
        except RuntimeError as e:
            print(f"Failed to spawn at spawn point {i}: {e}")
            continue
    
    print("Could not spawn ego vehicle at any spawn point!")
    return None

def spawn_npc_vehicles(world, blueprint_library, num_vehicles=10):
    """
    Spawn NPC vehicles around the map
    
    Args:
        world: CARLA world
        blueprint_library: CARLA blueprint library  
        num_vehicles: Number of NPC vehicles to spawn
    
    Returns:
        list: List of spawned NPC vehicle actors
    """
    npc_vehicles = []
    spawn_points = world.get_map().get_spawn_points()
    
    if len(spawn_points) < num_vehicles:
        num_vehicles = len(spawn_points)
        print(f"Reducing NPC vehicles to {num_vehicles} due to limited spawn points")
    
    vehicle_blueprints = blueprint_library.filter('vehicle.*')
    
    # Randomly select spawn points
    random.shuffle(spawn_points)
    
    for i in range(num_vehicles):
        try:
            npc_bp = random.choice(vehicle_blueprints)
            
            # Set random color if available
            if npc_bp.has_attribute('color'):
                color = random.choice(npc_bp.get_attribute('color').recommended_values)
                npc_bp.set_attribute('color', color)
            
            npc_vehicle = world.spawn_actor(npc_bp, spawn_points[i])
            npc_vehicles.append(npc_vehicle)
            
            # Set autopilot for NPC vehicles
            npc_vehicle.set_autopilot(True)
            
        except RuntimeError as e:
            print(f"Failed to spawn NPC vehicle {i}: {e}")
            continue
    
    print(f"Spawned {len(npc_vehicles)} NPC vehicles")
    return npc_vehicles

def setup_sensors(world, ego_vehicle):
    """
    Set up basic sensors (camera) on the ego vehicle
    
    Args:
        world: CARLA world
        ego_vehicle: The ego vehicle actor
    
    Returns:
        list: List of sensor actors
    """
    sensors = []
    blueprint_library = world.get_blueprint_library()
    
    # RGB Camera
    camera_bp = blueprint_library.find('sensor.camera.rgb')
    camera_bp.set_attribute('image_size_x', '800')
    camera_bp.set_attribute('image_size_y', '600')
    camera_bp.set_attribute('fov', '90')
    
    # Mount camera on the vehicle
    camera_transform = carla.Transform(
        carla.Location(x=2.0, z=1.4),  # 2 meters forward, 1.4 meters up
        carla.Rotation(pitch=0.0)      # No pitch
    )
    
    camera = world.spawn_actor(camera_bp, camera_transform, attach_to=ego_vehicle)
    sensors.append(camera)
    
    # Set up camera callback
    camera.listen(lambda image: image.save_to_disk('./sensor_data/camera_%06d.png' % image.frame))
    
    print("Camera sensor attached to ego vehicle")
    return sensors

def run_scenario(world, ego_vehicle, duration=60):
    """
    Run the basic scenario
    
    Args:
        world: CARLA world
        ego_vehicle: The ego vehicle actor
        duration: Scenario duration in seconds
    """
    print(f"Running scenario for {duration} seconds...")
    
    # Enable autopilot for ego vehicle 
    ego_vehicle.set_autopilot(True)
    
    # Set synchronous mode for consistent simulation
    original_settings = world.get_settings()
    settings = world.get_settings()
    settings.synchronous_mode = True
    settings.fixed_delta_seconds = 0.05  # 20 FPS
    world.apply_settings(settings)
    
    try:
        start_time = time.time()
        frame = 0
        
        while time.time() - start_time < duration:
            # Advance the simulation
            world.tick()
            frame += 1
            
            # Print status every 5 seconds
            if frame % 100 == 0:  # Every 5 seconds at 20 FPS
                elapsed = time.time() - start_time
                ego_location = ego_vehicle.get_location()
                ego_velocity = ego_vehicle.get_velocity()
                speed_ms = (ego_velocity.x**2 + ego_velocity.y**2 + ego_velocity.z**2)**0.5
                speed_kmh = speed_ms * 3.6
                
                print(f"Time: {elapsed:.1f}s | Location: ({ego_location.x:.1f}, {ego_location.y:.1f}) | Speed: {speed_kmh:.1f} km/h")
    
    finally:
        # Restore original settings
        world.apply_settings(original_settings)
        print("Scenario completed!")

def cleanup_actors(world, actors):
    """
    Clean up spawned actors
    
    Args:
        world: CARLA world
        actors: List of actors to destroy
    """
    print("Cleaning up actors...")
    for actor in actors:
        if actor is not None and actor.is_alive:
            actor.destroy()

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='OSM Map Scenario Runner')
    parser.add_argument(
        '--osm-path',
        required=True,
        help='Path to the OSM file to load'
    )
    parser.add_argument(
        '--host',
        default='127.0.0.1',
        help='IP of the host server (default: 127.0.0.1)'
    )
    parser.add_argument(
        '-p', '--port',
        default=2000,
        type=int,
        help='TCP port to listen to (default: 2000)'
    )
    parser.add_argument(
        '--duration',
        default=60,
        type=int,
        help='Scenario duration in seconds (default: 60)'
    )
    parser.add_argument(
        '--num-npc',
        default=10,
        type=int,
        help='Number of NPC vehicles to spawn (default: 10)'
    )
    
    args = parser.parse_args()
    
    # Create sensor data directory
    os.makedirs('./sensor_data', exist_ok=True)
    
    all_actors = []
    
    try:
        # Connect to CARLA server
        print(f"Connecting to CARLA server at {args.host}:{args.port}")
        client = carla.Client(args.host, args.port)
        client.set_timeout(30.0)
        
        # Test connection
        try:
            world = client.get_world()
            print("Successfully connected to CARLA server")
        except RuntimeError as e:
            print(f"Failed to connect to CARLA server: {e}")
            print("Make sure CARLA server is running!")
            return
        
        # Load OSM map
        world = load_osm_map(client, args.osm_path)
        
        # Wait a moment for the world to stabilize
        time.sleep(2)
        
        # Get blueprint library
        blueprint_library = world.get_blueprint_library()
        
        # Spawn ego vehicle
        ego_vehicle = spawn_ego_vehicle(world, blueprint_library)
        if ego_vehicle is None:
            print("Failed to spawn ego vehicle. Exiting.")
            return
        all_actors.append(ego_vehicle)
        
        # Spawn NPC vehicles
        npc_vehicles = spawn_npc_vehicles(world, blueprint_library, args.num_npc)
        all_actors.extend(npc_vehicles)
        
        # Setup sensors
        sensors = setup_sensors(world, ego_vehicle)
        all_actors.extend(sensors)
        
        # Run the scenario
        run_scenario(world, ego_vehicle, args.duration)
        
    except KeyboardInterrupt:
        print("\nScenario interrupted by user")
    
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Clean up all actors
        cleanup_actors(world, all_actors)
        print("Scenario finished!")

if __name__ == '__main__':
    main()