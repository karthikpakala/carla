#!/usr/bin/env python

"""
CARLA Scenario with Built-in Map

This script demonstrates how to run a basic scenario with CARLA's built-in maps.
Once this works, you can modify it to use OSM maps.

Usage:
    python basic_carla_scenario.py
"""

import carla
import random
import time
import argparse

def spawn_ego_vehicle(world, blueprint_library):
    """Spawn the ego vehicle at a random spawn point"""
    vehicle_blueprints = blueprint_library.filter('vehicle.*')
    ego_bp = random.choice(vehicle_blueprints)
    
    if ego_bp.has_attribute('color'):
        color = random.choice(ego_bp.get_attribute('color').recommended_values)
        ego_bp.set_attribute('color', color)
    
    spawn_points = world.get_map().get_spawn_points()
    
    if not spawn_points:
        print("No spawn points available!")
        return None
    
    spawn_point = random.choice(spawn_points)
    
    try:
        ego_vehicle = world.spawn_actor(ego_bp, spawn_point)
        print(f"Ego vehicle spawned at: {spawn_point.location}")
        return ego_vehicle
    except RuntimeError as e:
        print(f"Failed to spawn ego vehicle: {e}")
        return None

def spawn_npc_vehicles(world, blueprint_library, num_vehicles=5):
    """Spawn NPC vehicles around the map"""
    npc_vehicles = []
    spawn_points = world.get_map().get_spawn_points()
    
    if len(spawn_points) < num_vehicles:
        num_vehicles = len(spawn_points)
    
    vehicle_blueprints = blueprint_library.filter('vehicle.*')
    random.shuffle(spawn_points)
    
    for i in range(num_vehicles):
        try:
            npc_bp = random.choice(vehicle_blueprints)
            
            if npc_bp.has_attribute('color'):
                color = random.choice(npc_bp.get_attribute('color').recommended_values)
                npc_bp.set_attribute('color', color)
            
            npc_vehicle = world.spawn_actor(npc_bp, spawn_points[i])
            npc_vehicles.append(npc_vehicle)
            npc_vehicle.set_autopilot(True)
            
        except RuntimeError as e:
            print(f"Failed to spawn NPC vehicle {i}: {e}")
            continue
    
    print(f"Spawned {len(npc_vehicles)} NPC vehicles")
    return npc_vehicles

def setup_camera_sensor(world, ego_vehicle):
    """Set up a camera sensor on the ego vehicle"""
    blueprint_library = world.get_blueprint_library()
    camera_bp = blueprint_library.find('sensor.camera.rgb')
    camera_bp.set_attribute('image_size_x', '800')
    camera_bp.set_attribute('image_size_y', '600')
    camera_bp.set_attribute('fov', '90')
    
    camera_transform = carla.Transform(
        carla.Location(x=2.0, z=1.4),
        carla.Rotation(pitch=0.0)
    )
    
    camera = world.spawn_actor(camera_bp, camera_transform, attach_to=ego_vehicle)
    
    # Create output directory
    import os
    os.makedirs('./sensor_data', exist_ok=True)
    
    # Set up callback to save images
    camera.listen(lambda image: image.save_to_disk('./sensor_data/camera_%06d.png' % image.frame))
    
    print("Camera sensor attached and saving to ./sensor_data/")
    return camera

def run_scenario(world, ego_vehicle, duration=30):
    """Run the basic scenario"""
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

def cleanup_actors(actors):
    """Clean up spawned actors"""
    print("Cleaning up actors...")
    for actor in actors:
        if actor is not None and actor.is_alive:
            actor.destroy()

def main():
    parser = argparse.ArgumentParser(description='CARLA Basic Scenario')
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
        default=30,
        type=int,
        help='Scenario duration in seconds (default: 30)'
    )
    parser.add_argument(
        '--num-npc',
        default=5,
        type=int,
        help='Number of NPC vehicles to spawn (default: 5)'
    )
    parser.add_argument(
        '--map',
        default=None,
        help='Map to load (default: current map)'
    )
    
    args = parser.parse_args()
    
    all_actors = []
    
    try:
        # Connect to CARLA server
        print(f"Connecting to CARLA server at {args.host}:{args.port}")
        client = carla.Client(args.host, args.port)
        client.set_timeout(10.0)
        
        # Get world
        world = client.get_world()
        print(f"Connected! Current map: {world.get_map().name}")
        
        # Load different map if requested
        if args.map:
            print(f"Loading map: {args.map}")
            world = client.load_world(args.map)
            time.sleep(2)  # Wait for map to load
        
        # Get blueprint library
        blueprint_library = world.get_blueprint_library()
        
        # Show available spawn points
        spawn_points = world.get_map().get_spawn_points()
        print(f"Available spawn points: {len(spawn_points)}")
        
        # Spawn ego vehicle
        ego_vehicle = spawn_ego_vehicle(world, blueprint_library)
        if ego_vehicle is None:
            print("Failed to spawn ego vehicle. Exiting.")
            return
        all_actors.append(ego_vehicle)
        
        # Spawn NPC vehicles
        npc_vehicles = spawn_npc_vehicles(world, blueprint_library, args.num_npc)
        all_actors.extend(npc_vehicles)
        
        # Setup camera sensor
        camera = setup_camera_sensor(world, ego_vehicle)
        all_actors.append(camera)
        
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
        cleanup_actors(all_actors)
        print("Scenario finished!")

if __name__ == '__main__':
    main()