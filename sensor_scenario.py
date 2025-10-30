#!/usr/bin/env python3

"""
CARLA Sensor Data Collection Scenario
This creates a vehicle with multiple sensors and collects data
"""

import carla
import random
import time
import sys
import os
import weakref

def main():
    actors = []
    sensor_data = {'images_saved': 0, 'lidar_saved': 0}
    
    try:
        print("📸 Starting CARLA Sensor Data Collection Scenario")
        print("=" * 65)
        
        # Connect to CARLA
        client = carla.Client('localhost', 2000)
        client.set_timeout(10.0)
        world = client.get_world()
        
        print(f"✓ Connected to CARLA!")
        print(f"✓ Map: {world.get_map().name}")
        
        # Create output directory
        output_dir = "/home/karthik.pakala@torc.ai/carla/sensor_data"
        os.makedirs(output_dir, exist_ok=True)
        print(f"✓ Output directory: {output_dir}")
        
        # Get resources
        blueprint_library = world.get_blueprint_library()
        spawn_points = world.get_map().get_spawn_points()
        
        # Spawn main vehicle
        print(f"\n🚗 Spawning main vehicle...")
        vehicle_bp = blueprint_library.find('vehicle.tesla.model3')
        if vehicle_bp.has_attribute('color'):
            vehicle_bp.set_attribute('color', '0,0,255')  # Blue
        
        spawn_point = random.choice(spawn_points)
        vehicle = world.spawn_actor(vehicle_bp, spawn_point)
        actors.append(vehicle)
        vehicle.set_autopilot(True)
        
        print(f"✓ Vehicle spawned: {vehicle.type_id} (ID: {vehicle.id})")
        print(f"✓ Location: ({spawn_point.location.x:.1f}, {spawn_point.location.y:.1f})")
        
        # Add RGB Camera
        print(f"\n📷 Adding RGB Camera...")
        camera_bp = blueprint_library.find('sensor.camera.rgb')
        camera_bp.set_attribute('image_size_x', '800')
        camera_bp.set_attribute('image_size_y', '600')
        camera_bp.set_attribute('fov', '90')
        
        camera_transform = carla.Transform(
            carla.Location(x=1.5, z=2.4),
            carla.Rotation(pitch=-15)
        )
        
        camera = world.spawn_actor(camera_bp, camera_transform, attach_to=vehicle)
        actors.append(camera)
        
        # Camera callback
        def save_rgb_image(image):
            sensor_data['images_saved'] += 1
            image.save_to_disk(f'{output_dir}/rgb_{image.frame:06d}.png')
        
        camera.listen(save_rgb_image)
        print(f"✓ RGB Camera attached (ID: {camera.id})")
        
        # Add Depth Camera
        print(f"🔍 Adding Depth Camera...")
        depth_bp = blueprint_library.find('sensor.camera.depth')
        depth_bp.set_attribute('image_size_x', '800')
        depth_bp.set_attribute('image_size_y', '600')
        
        depth_camera = world.spawn_actor(depth_bp, camera_transform, attach_to=vehicle)
        actors.append(depth_camera)
        
        # Depth camera callback
        def save_depth_image(image):
            sensor_data['depth_saved'] = sensor_data.get('depth_saved', 0) + 1
            image.save_to_disk(f'{output_dir}/depth_{image.frame:06d}.png', carla.ColorConverter.LogarithmicDepth)
        
        depth_camera.listen(save_depth_image)
        print(f"✓ Depth Camera attached (ID: {depth_camera.id})")
        
        # Add LiDAR
        print(f"🔄 Adding LiDAR...")
        lidar_bp = blueprint_library.find('sensor.lidar.ray_cast')
        lidar_bp.set_attribute('channels', '32')
        lidar_bp.set_attribute('points_per_second', '90000')
        lidar_bp.set_attribute('rotation_frequency', '40')
        lidar_bp.set_attribute('range', '20')
        
        lidar_transform = carla.Transform(carla.Location(x=0, z=2.0))
        lidar = world.spawn_actor(lidar_bp, lidar_transform, attach_to=vehicle)
        actors.append(lidar)
        
        # LiDAR callback
        def save_lidar_data(point_cloud):
            sensor_data['lidar_saved'] += 1
            point_cloud.save_to_disk(f'{output_dir}/lidar_{point_cloud.frame:06d}.ply')
        
        lidar.listen(save_lidar_data)
        print(f"✓ LiDAR attached (ID: {lidar.id})")
        
        # Spawn some NPC vehicles for interesting data
        print(f"\n🚙 Adding NPC vehicles...")
        npc_count = 0
        for i in range(5):
            try:
                npc_bp = random.choice(blueprint_library.filter('vehicle.*'))
                npc_spawn = random.choice(spawn_points)
                npc = world.try_spawn_actor(npc_bp, npc_spawn)
                if npc:
                    actors.append(npc)
                    npc.set_autopilot(True)
                    npc_count += 1
            except:
                pass
        
        print(f"✓ Added {npc_count} NPC vehicles")
        
        # Run data collection
        print(f"\n📊 Collecting sensor data for 25 seconds...")
        print("-" * 65)
        
        start_time = time.time()
        while time.time() - start_time < 25:
            elapsed = time.time() - start_time
            
            # Get vehicle status
            location = vehicle.get_location()
            velocity = vehicle.get_velocity()
            speed = 3.6 * (velocity.x**2 + velocity.y**2 + velocity.z**2)**0.5
            
            print(f"[{elapsed:5.1f}s] Pos: ({location.x:6.1f}, {location.y:6.1f}) | "
                  f"Speed: {speed:5.1f} km/h | "
                  f"RGB: {sensor_data['images_saved']:3d} | "
                  f"Depth: {sensor_data.get('depth_saved', 0):3d} | "
                  f"LiDAR: {sensor_data['lidar_saved']:3d}")
            
            time.sleep(2)
        
        print(f"\n🎉 Data collection completed!")
        print(f"📁 Output directory: {output_dir}")
        print(f"📈 Data collected:")
        print(f"   • RGB images: {sensor_data['images_saved']}")
        print(f"   • Depth images: {sensor_data.get('depth_saved', 0)}")
        print(f"   • LiDAR scans: {sensor_data['lidar_saved']}")
        
    except KeyboardInterrupt:
        print("\n⏹️  Data collection interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    finally:
        # Cleanup
        print(f"\n🧹 Cleaning up...")
        for actor in actors:
            try:
                if hasattr(actor, 'is_alive') and actor.is_alive:
                    actor.destroy()
            except:
                pass
        print("✓ Cleanup complete!")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())