#!/usr/bin/env python3

"""
CARLA Traffic Generation Scenario
This creates a busy traffic environment with multiple vehicles
"""

import carla
import random
import time
import sys

def main():
    actors = []
    
    try:
        print("🚦 Starting CARLA Traffic Generation Scenario")
        print("=" * 60)
        
        # Connect to CARLA
        client = carla.Client('localhost', 2000)
        client.set_timeout(10.0)
        world = client.get_world()
        
        print(f"✓ Connected to CARLA!")
        print(f"✓ Map: {world.get_map().name}")
        
        # Get resources
        blueprint_library = world.get_blueprint_library()
        spawn_points = world.get_map().get_spawn_points()
        vehicle_blueprints = blueprint_library.filter('vehicle.*')
        
        print(f"✓ Available spawn points: {len(spawn_points)}")
        print(f"✓ Available vehicles: {len(vehicle_blueprints)}")
        
        # Spawn multiple vehicles
        num_vehicles = min(20, len(spawn_points))  # Don't exceed spawn points
        print(f"\n🚗 Spawning {num_vehicles} vehicles...")
        
        spawned_vehicles = 0
        used_spawn_points = set()
        
        for i in range(num_vehicles):
            try:
                # Select random vehicle blueprint
                vehicle_bp = random.choice(vehicle_blueprints)
                
                # Set random color if available
                if vehicle_bp.has_attribute('color'):
                    color = random.choice(vehicle_bp.get_attribute('color').recommended_values)
                    vehicle_bp.set_attribute('color', color)
                
                # Find unused spawn point
                attempts = 0
                while attempts < 10:  # Try up to 10 times
                    spawn_point = random.choice(spawn_points)
                    spawn_key = (round(spawn_point.location.x), round(spawn_point.location.y))
                    
                    if spawn_key not in used_spawn_points:
                        used_spawn_points.add(spawn_key)
                        break
                    attempts += 1
                
                if attempts >= 10:
                    print(f"   ⚠️  Vehicle {i+1}: Could not find free spawn point")
                    continue
                
                # Try to spawn vehicle
                vehicle = world.try_spawn_actor(vehicle_bp, spawn_point)
                
                if vehicle is not None:
                    actors.append(vehicle)
                    vehicle.set_autopilot(True)
                    spawned_vehicles += 1
                    
                    print(f"   ✓ Vehicle {spawned_vehicles:2d}: {vehicle_bp.id} (ID: {vehicle.id})")
                else:
                    print(f"   ⚠️  Vehicle {i+1}: Spawn failed (location occupied)")
                    
            except Exception as e:
                print(f"   ❌ Vehicle {i+1}: Error - {e}")
        
        print(f"\n✅ Successfully spawned {spawned_vehicles} vehicles")
        
        if spawned_vehicles == 0:
            print("❌ No vehicles spawned. Exiting...")
            return 1
        
        # Monitor traffic for 30 seconds
        print(f"\n📊 Monitoring traffic for 30 seconds...")
        print("-" * 60)
        
        start_time = time.time()
        while time.time() - start_time < 30:
            elapsed = time.time() - start_time
            
            # Get statistics
            moving_vehicles = 0
            total_speed = 0
            active_vehicles = []
            
            for vehicle in actors:
                if vehicle.is_alive:
                    active_vehicles.append(vehicle)
                    velocity = vehicle.get_velocity()
                    speed = 3.6 * (velocity.x**2 + velocity.y**2 + velocity.z**2)**0.5
                    total_speed += speed
                    if speed > 1.0:  # Consider moving if > 1 km/h
                        moving_vehicles += 1
            
            avg_speed = total_speed / len(active_vehicles) if active_vehicles else 0
            
            print(f"[{elapsed:5.1f}s] Active: {len(active_vehicles):2d} | "
                  f"Moving: {moving_vehicles:2d} | "
                  f"Avg Speed: {avg_speed:5.1f} km/h")
            
            time.sleep(2)
        
        print(f"\n🎉 Traffic scenario completed!")
        print(f"📈 Final stats: {len(active_vehicles)} vehicles active")
        
    except KeyboardInterrupt:
        print("\n⏹️  Scenario interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    finally:
        # Cleanup
        print(f"\n🧹 Cleaning up {len(actors)} actors...")
        destroyed = 0
        for actor in actors:
            try:
                if actor.is_alive:
                    actor.destroy()
                    destroyed += 1
            except Exception as e:
                print(f"   ⚠️  Error destroying actor: {e}")
        
        print(f"✓ Destroyed {destroyed} actors")
        print("✓ Cleanup complete!")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())