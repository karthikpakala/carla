#!/usr/bin/env python3

"""
Stable CARLA scenario - Basic vehicle spawning and monitoring
"""

import carla
import random
import time
import sys

def main():
    actors = []
    
    try:
        print("🚗 Starting CARLA Basic Scenario")
        print("=" * 50)
        
        # Connect to CARLA
        client = carla.Client('localhost', 2000)
        client.set_timeout(10.0)
        world = client.get_world()
        
        print(f"✓ Connected to CARLA!")
        print(f"✓ Current map: {world.get_map().name}")
        
        # Get blueprint library and spawn points
        blueprint_library = world.get_blueprint_library()
        spawn_points = world.get_map().get_spawn_points()
        print(f"✓ Found {len(spawn_points)} spawn points")
        
        # Find a Tesla Model 3 (reliable vehicle)
        tesla_bp = None
        for bp in blueprint_library.filter('vehicle.*'):
            if 'tesla' in bp.id and 'model3' in bp.id:
                tesla_bp = bp
                break
        
        if tesla_bp is None:
            print("Tesla not found, using random vehicle...")
            tesla_bp = random.choice(blueprint_library.filter('vehicle.*'))
        
        print(f"✓ Selected vehicle: {tesla_bp.id}")
        
        # Set vehicle color
        if tesla_bp.has_attribute('color'):
            tesla_bp.set_attribute('color', '255,0,0')  # Red
            print("✓ Set vehicle color to red")
        
        # Spawn the vehicle
        spawn_point = random.choice(spawn_points)
        vehicle = world.spawn_actor(tesla_bp, spawn_point)
        actors.append(vehicle)
        
        print(f"✓ Vehicle spawned at: ({spawn_point.location.x:.1f}, {spawn_point.location.y:.1f})")
        print(f"✓ Vehicle ID: {vehicle.id}")
        
        # Enable autopilot
        vehicle.set_autopilot(True)
        print("✓ Autopilot enabled")
        
        # Monitor the vehicle for 20 seconds
        print("\n📊 Monitoring vehicle for 20 seconds...")
        print("-" * 50)
        
        start_time = time.time()
        while time.time() - start_time < 20:
            # Get vehicle status
            location = vehicle.get_location()
            velocity = vehicle.get_velocity()
            speed_kmh = 3.6 * (velocity.x**2 + velocity.y**2 + velocity.z**2)**0.5
            
            elapsed = time.time() - start_time
            print(f"[{elapsed:5.1f}s] Pos: ({location.x:6.1f}, {location.y:6.1f}, {location.z:4.1f}) | Speed: {speed_kmh:5.1f} km/h")
            
            time.sleep(2)
        
        print("\n🎉 Scenario completed successfully!")
        
    except KeyboardInterrupt:
        print("\n⏹️  Scenario interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1
    
    finally:
        # Cleanup
        print("\n🧹 Cleaning up...")
        for actor in actors:
            if actor.is_alive:
                actor.destroy()
                print(f"✓ Destroyed {actor.type_id}")
        print("✓ Cleanup complete!")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())