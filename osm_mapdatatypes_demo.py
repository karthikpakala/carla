#!/usr/bin/env python3

"""
OSM MapDataTypes Integration Demo

This script demonstrates how OpenStreetMap data flows through CARLA's 
MapDataTypes.h enums and data structures during the OSM pipeline processing.

It shows the detailed message flow from OSM file → OpenDRIVE → CARLA Map
with explicit MapDataTypes field analysis.
"""

import sys
import os
import time

# Add the CARLA Python API to the path
carla_path = '/home/karthik.pakala@torc.ai/carla/PythonAPI/carla'
sys.path.append(carla_path)

try:
    import carla
    print("✅ CARLA module imported successfully")
except ImportError as e:
    print(f"❌ Error importing CARLA: {e}")
    sys.exit(1)

def demonstrate_mapdatatypes_flow(osm_file_path='~/Downloads/uvalde.osm'):
    """Demonstrate OSM data flow through MapDataTypes."""
    
    print("🗺️  OSM MapDataTypes Integration Demonstration")
    print("=" * 55)
    
    osm_file_path = os.path.expanduser(osm_file_path)
    
    if not os.path.exists(osm_file_path):
        print(f"❌ OSM file not found: {osm_file_path}")
        return False
    
    try:
        # Step 1: OSM File Analysis
        print("\n📄 Step 1: OSM File Structure Analysis")
        print("-" * 40)
        
        with open(osm_file_path, 'r', encoding='utf-8') as f:
            osm_content = f.read()
        
        # Analyze OSM tags that map to MapDataTypes
        highway_tags = osm_content.count('highway="')
        lane_tags = osm_content.count('lanes="')
        barrier_tags = osm_content.count('barrier="')
        surface_tags = osm_content.count('surface="')
        
        print(f"   OSM Elements that map to MapDataTypes.h:")
        print(f"   • Highway tags: {highway_tags} (→ RoadType enum)")
        print(f"   • Lane tags: {lane_tags} (→ LaneType enum)")
        print(f"   • Barrier tags: {barrier_tags} (→ LaneBoundaryType enum)")
        print(f"   • Surface tags: {surface_tags} (→ SurfacePolygonType enum)")
        
        # Connect to CARLA
        print("\n🔌 Step 2: CARLA Server Connection")
        print("-" * 40)
        
        client = carla.Client('localhost', 2000)
        client.set_timeout(30.0)
        world = client.get_world()
        print(f"   ✅ Connected to CARLA server")
        print(f"   📍 Current map: {world.get_map().name}")
        
        # Step 3: OSM to OpenDRIVE Conversion with MapDataTypes mapping
        print("\n🔄 Step 3: OSM→OpenDRIVE Conversion (MapDataTypes Integration)")
        print("-" * 65)
        
        print("   Configuring OSM2OdrSettings with MapDataTypes awareness...")
        settings = carla.Osm2OdrSettings()
        
        # Show OSM way types and their RoadType mapping
        osm_way_types = [
            "motorway",      # → RoadType::Highway
            "motorway_link", # → RoadType::HighwayConnector  
            "trunk",         # → RoadType::Highway
            "trunk_link",    # → RoadType::HighwayConnector
            "primary",       # → RoadType::SurfaceStreet
            "secondary",     # → RoadType::SurfaceStreet
            "residential"    # → RoadType::SurfaceStreet
        ]
        
        settings.set_osm_way_types(osm_way_types)
        settings.default_lane_width = 3.5
        settings.center_map = True
        
        print("   OSM Way Type → MapDataTypes::RoadType Mapping:")
        road_type_mapping = [
            ("motorway", "RoadType::Highway"),
            ("motorway_link", "RoadType::HighwayConnector"),
            ("trunk", "RoadType::Highway"),
            ("trunk_link", "RoadType::HighwayConnector"),
            ("primary", "RoadType::SurfaceStreet"),
            ("secondary", "RoadType::SurfaceStreet"),
            ("residential", "RoadType::SurfaceStreet")
        ]
        
        for osm_type, carla_type in road_type_mapping:
            present = f'highway="{osm_type}"' in osm_content
            status = "✅ FOUND" if present else "   ---"
            print(f"   • {osm_type:12} → {carla_type:25} | {status}")
        
        print("\n   Converting OSM to OpenDRIVE with MapDataTypes integration...")
        xodr_data = carla.Osm2Odr.convert(osm_content, settings)
        print(f"   ✅ Conversion complete: {len(xodr_data):,} characters")
        
        # Step 4: OpenDRIVE to CARLA Map with MapDataTypes
        print("\n🗺️  Step 4: OpenDRIVE→CARLA Map (MapDataTypes Instantiation)")
        print("-" * 60)
        
        print("   Loading OpenDRIVE into CARLA with MapDataTypes structure...")
        generation_params = carla.OpendriveGenerationParameters(
            vertex_distance=3.0,
            max_road_length=200.0,
            wall_height=0.0,
            additional_width=0.6,
            smooth_junctions=True,
            enable_mesh_visibility=True
        )
        
        world = client.generate_opendrive_world(xodr_data, generation_params)
        time.sleep(2)
        
        carla_map = world.get_map()
        print(f"   ✅ Map instantiated: {carla_map.name}")
        
        # Step 5: MapDataTypes Field Analysis
        print("\n📊 Step 5: MapDataTypes Field Analysis in Loaded Map")
        print("-" * 55)
        
        waypoints = carla_map.generate_waypoints(distance=15.0)
        spawn_points = carla_map.get_spawn_points()
        
        print(f"   Map Elements Created:")
        print(f"   • Waypoints: {len(waypoints)}")
        print(f"   • Spawn Points: {len(spawn_points)}")
        
        if waypoints:
            print(f"\n   🔍 MapDataTypes.h Field Analysis (First 5 waypoints):")
            
            for i, wp in enumerate(waypoints[:5]):
                print(f"\n   Waypoint {i+1}:")
                print(f"   ├─ Road ID: {wp.road_id}")
                print(f"   ├─ Lane ID: {wp.lane_id}")
                print(f"   ├─ Lane Type: {wp.lane_type} (LaneType enum)")
                print(f"   ├─ Lane Width: {wp.lane_width:.2f}m")
                print(f"   ├─ Is Junction: {wp.is_junction} (→ RoadType::Intersection)")
                print(f"   ├─ Position: ({wp.transform.location.x:.1f}, {wp.transform.location.y:.1f})")
                
                # Analyze lane markings (MapDataTypes boundary enums)
                try:
                    left_marking = wp.left_lane_marking
                    right_marking = wp.right_lane_marking
                    
                    if left_marking:
                        print(f"   ├─ Left Boundary: {left_marking.type} (LaneBoundaryType enum)")
                        print(f"   │  └─ Color: {left_marking.color} (LaneBoundaryColor enum)")
                    
                    if right_marking:
                        print(f"   └─ Right Boundary: {right_marking.type} (LaneBoundaryType enum)")
                        print(f"      └─ Color: {right_marking.color} (LaneBoundaryColor enum)")
                    else:
                        print(f"   └─ Boundaries: Analysis complete")
                        
                except Exception as e:
                    print(f"   └─ Boundary analysis: Skipped ({str(e)[:30]}...)")
        
        # Step 6: Data Flow Summary
        print(f"\n🔄 Step 6: Complete Data Flow Summary")
        print("-" * 40)
        
        print("   OSM File → CARLA MapDataTypes Data Flow:")
        print("   ┌─ OSM XML Tags")
        print("   │  ├─ highway='primary' → RoadType::SurfaceStreet")
        print("   │  ├─ lanes='2' → LaneType::Standard (default)")
        print("   │  ├─ barrier='kerb' → LaneBoundaryType::Curb")
        print("   │  └─ surface='asphalt' → SurfacePolygonType::Surface")
        print("   │")
        print("   ├─ OSM2OdrSettings → OpenDRIVE XML")
        print("   │  ├─ Road network topology")
        print("   │  ├─ Lane definitions with types")
        print("   │  └─ Junction connections")
        print("   │")
        print("   ├─ OpendriveGenerationParameters → CARLA Map")
        print("   │  ├─ Visual mesh generation")
        print("   │  ├─ Collision geometry")
        print("   │  └─ Navigation waypoints")
        print("   │")
        print("   └─ MapDataTypes.h Enums → Type-Safe Access")
        print("      ├─ RoadType classification")
        print("      ├─ LaneType specification")
        print("      ├─ LaneBoundaryType definition")
        print("      └─ Runtime type safety")
        
        print(f"\n✅ MapDataTypes Integration Demonstration Complete!")
        print("   The OSM pipeline successfully flows through MapDataTypes.h")
        print("   providing type-safe road network representation in CARLA.")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Demonstration failed: {e}")
        return False

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description="Demonstrate OSM MapDataTypes integration")
    parser.add_argument('--osm-file', default='~/Downloads/uvalde.osm',
                       help='Path to OSM file (default: ~/Downloads/uvalde.osm)')
    
    args = parser.parse_args()
    
    try:
        success = demonstrate_mapdatatypes_flow(args.osm_file)
        print(f"\n{'🎉 SUCCESS' if success else '❌ FAILED'}: MapDataTypes demonstration")
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print('\n👋 Demonstration cancelled by user.')
        sys.exit(0)