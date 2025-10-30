#!/usr/bin/env python3

"""
Simple CARLA scenario with multiple vehicles and sensors
"""

import carla
import random
import time
import sys
import os

def main():
    # List to keep references to all spawned actors
    actor_list = []
    
    try:
        # Connect to the CARLA server
        print("Connecting to CARLA server...")
        client = carla.Client('localhost', 2000)
        client.set_timeout(10.0)
        
        # Get the world
        world = client.get_world()
        print(f"Connected successfully! Current map: {world.get_map().name}")
        
        # Get the blueprint library
        blueprint_library = world.get_blueprint_library()
        
        # Get available spawn points
        spawn_points = world.get_map().get_spawn_points()
        print(f"Available spawn points: {len(spawn_points)}")
        
        # === SCENARIO 1: Spawn a main vehicle with autopilot ===
        print("\n=== Spawning main vehicle ===")
        
        # Choose a random vehicle blueprint
        vehicle_bp = random.choice(blueprint_library.filter('vehicle.tesla.model3'))
        
        # Set some attributes
        if vehicle_bp.has_attribute('color'):
            color = random.choice(vehicle_bp.get_attribute('color').recommended_values)
            vehicle_bp.set_attribute('color', color)
            print(f"Vehicle color set to: {color}")
        
        # Choose a spawn point
        spawn_point = random.choice(spawn_points)
        print(f"Spawning at: {spawn_point.location}")
        
        # Spawn the main vehicle
        main_vehicle = world.spawn_actor(vehicle_bp, spawn_point)
        actor_list.append(main_vehicle)
        print(f"Main vehicle spawned: {main_vehicle.type_id} (ID: {main_vehicle.id})")
        
        # Enable autopilot
        main_vehicle.set_autopilot(True)
        print("Autopilot enabled for main vehicle")
        
        # === SCENARIO 2: Add a camera sensor ===
        print("\n=== Adding camera sensor ===")
        
        # Get RGB camera blueprint
        camera_bp = blueprint_library.find('sensor.camera.rgb')
        camera_bp.set_attribute('image_size_x', '800')
        camera_bp.set_attribute('image_size_y', '600')
        camera_bp.set_attribute('fov', '90')
        
        # Set camera transform (relative to vehicle)
        camera_transform = carla.Transform(
            carla.Location(x=1.5, z=2.4),  # 1.5m forward, 2.4m up
            carla.Rotation(pitch=-15)       # Look slightly down
        )
        
        # Spawn camera attached to vehicle
        camera = world.spawn_actor(camera_bp, camera_transform, attach_to=main_vehicle)
        actor_list.append(camera)
        print(f"Camera spawned: {camera.type_id} (ID: {camera.id})")
        
        # Create output directory for images
        output_dir = "/home/karthik.pakala@torc.ai/carla/scenario_output"
        os.makedirs(output_dir, exist_ok=True)
        
        # Save images to disk
        camera.listen(lambda image: image.save_to_disk(f'{output_dir}/rgb_%06d.png' % image.frame))
        print(f"Camera images will be saved to: {output_dir}")
        
        # === SCENARIO 3: Add some NPC vehicles ===
        print("\n=== Spawning NPC vehicles ===")
        
        # Spawn 5 NPC vehicles
        for i in range(5):
            try:
                # Choose random vehicle blueprint
                npc_bp = random.choice(blueprint_library.filter('vehicle.*'))
                
                # Set random color
                if npc_bp.has_attribute('color'):
                    color = random.choice(npc_bp.get_attribute('color').recommended_values)
                    npc_bp.set_attribute('color', color)
                
                # Choose random spawn point (different from main vehicle)
                npc_spawn_point = random.choice(spawn_points)
                
                # Try to spawn NPC vehicle
                npc_vehicle = world.try_spawn_actor(npc_bp, npc_spawn_point)
                
                if npc_vehicle is not None:
                    actor_list.append(npc_vehicle)
                    npc_vehicle.set_autopilot(True)
                    print(f"NPC {i+1} spawned: {npc_vehicle.type_id} (ID: {npc_vehicle.id})")
                else:
                    print(f"NPC {i+1}: Failed to spawn (spawn point may be occupied)")
                    
            except Exception as e:
                print(f"Error spawning NPC {i+1}: {e}")
        
        # === SCENARIO 4: Monitor the scenario ===
        print("\n=== Running scenario for 30 seconds ===")
        print("Main vehicle is driving around with autopilot...")
        print("Camera is recording images...")
        print("NPC vehicles are also moving...")
        
        # Run the scenario for 30 seconds
        start_time = time.time()
        while time.time() - start_time < 30:
            # Get vehicle location and velocity
            location = main_vehicle.get_location()
            velocity = main_vehicle.get_velocity()
            speed = 3.6 * (velocity.x**2 + velocity.y**2 + velocity.z**2)**0.5  # Convert to km/h
            
            print(f"Time: {time.time() - start_time:.1f}s | "
                  f"Position: ({location.x:.1f}, {location.y:.1f}, {location.z:.1f}) | "
                  f"Speed: {speed:.1f} km/h")
            
            time.sleep(2)
        
        print("\n=== Scenario completed successfully! ===")
        print(f"Total actors spawned: {len(actor_list)}")
        
    except KeyboardInterrupt:
        print("\nScenario interrupted by user")
    except Exception as e:
        print(f"Error during scenario: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Clean up all actors
        print("\n=== Cleaning up actors ===")
        for actor in actor_list:
            try:
                actor.destroy()
                print(f"Destroyed: {actor.type_id} (ID: {actor.id})")
            except Exception as e:
                print(f"Error destroying actor: {e}")
        
        print("Cleanup completed!")

if __name__ == '__main__':
    main()