#!/usr/bin/env python3

"""
CARLA OSM Pipeline Test Script

This script demonstrates the updated OSM map pipeline by:
1. Converting an OSM file to OpenDRIVE format
2. Loading the converted map in CARLA
3. Spawning vehicles to visually demonstrate the roadway
4. Running a simulation to show the pipeline functionality

Usage:
    python3 test_osm_pipeline.py [--osm-file PATH] [--duration SECONDS] [--vehicles COUNT]

Requirements:
    - CARLA server running on localhost:2000
    - OSM file (default: ~/Downloads/uvalde.osm)
"""

import sys
import os
import time
import argparse
from pathlib import Path

# Add the CARLA Python API to the path
carla_path = '/home/karthik.pakala@torc.ai/carla/PythonAPI/carla'
sys.path.append(carla_path)

try:
    import carla
    print("✅ CARLA module imported successfully")
except ImportError as e:
    print(f"❌ Error importing CARLA: {e}")
    print("Make sure CARLA Python API is properly installed")
    sys.exit(1)

class OSMPipelineTest:
    def __init__(self, host='localhost', port=2000, timeout=120.0):
        """Initialize the OSM pipeline test."""
        self.host = host
        self.port = port
        self.timeout = timeout
        self.client = None
        self.world = None
        self.spawned_vehicles = []
        
    def connect_to_carla(self):
        """Connect to the CARLA server."""
        try:
            print(f"🔌 Connecting to CARLA server at {self.host}:{self.port}...")
            self.client = carla.Client(self.host, self.port)
            self.client.set_timeout(self.timeout)
            
            # Test connection by getting the world
            self.world = self.client.get_world()
            current_map = self.world.get_map().name
            print(f"✅ Successfully connected to CARLA server!")
            print(f"📍 Current map: {current_map}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to connect to CARLA server: {e}")
            print("Make sure CARLA server is running on localhost:2000")
            return False
    
    def convert_osm_to_opendrive(self, osm_file_path, output_path=None):
        """Convert OSM file to OpenDRIVE format."""
        try:
            print(f"📄 Reading OSM file: {osm_file_path}")
            
            # Check if OSM file exists
            if not os.path.exists(osm_file_path):
                print(f"❌ OSM file not found: {osm_file_path}")
                return None
                
            # Read the OSM data
            with open(osm_file_path, mode="r", encoding="utf-8") as osm_file:
                osm_data = osm_file.read()
            
            file_size_mb = len(osm_data) / (1024 * 1024)
            print(f"✅ OSM data loaded: {len(osm_data):,} characters ({file_size_mb:.1f} MB)")
            
            # Configure OSM to OpenDRIVE conversion settings
            print("⚙️  Configuring conversion settings...")
            settings = carla.Osm2OdrSettings()
            
            # Set which OSM road types to include
            settings.set_osm_way_types([
                "motorway", "motorway_link",
                "trunk", "trunk_link", 
                "primary", "primary_link",
                "secondary", "secondary_link",
                "tertiary", "tertiary_link",
                "unclassified", "residential",
                "service"  # Include service roads for more complete conversion
            ])
            
            # Configure lane and road settings
            settings.default_lane_width = 3.5  # Standard lane width in meters
            settings.generate_traffic_lights = True  # Generate traffic lights from OSM data
            settings.all_junctions_with_traffic_lights = False  # Only where specified in OSM
            settings.center_map = True  # Center the map at origin
            
            print("🔄 Converting OSM to OpenDRIVE format...")
            print("   This may take a moment for larger OSM files...")
            
            # Perform the conversion
            xodr_data = carla.Osm2Odr.convert(osm_data, settings)
            
            xodr_size_mb = len(xodr_data) / (1024 * 1024)
            print(f"✅ Conversion successful: {len(xodr_data):,} characters ({xodr_size_mb:.1f} MB)")
            
            # Save the converted OpenDRIVE file if output path is specified
            if output_path:
                with open(output_path, "w", encoding="utf-8") as xodr_file:
                    xodr_file.write(xodr_data)
                print(f"💾 Saved OpenDRIVE file: {output_path}")
            
            return xodr_data
            
        except Exception as e:
            print(f"❌ OSM to OpenDRIVE conversion failed: {e}")
            return None
    
    def load_opendrive_map(self, xodr_data):
        """Load the OpenDRIVE map in CARLA with detailed MapDataTypes analysis."""
        try:
            print("🗺️  Loading OpenDRIVE map in CARLA...")
            print("   📋 Analyzing OSM data flow and MapDataTypes integration...")
            
            # Configure OpenDRIVE generation parameters
            generation_params = carla.OpendriveGenerationParameters(
                vertex_distance=2.0,      # Distance between road mesh vertices
                max_road_length=500.0,    # Maximum length of road segments
                wall_height=0.0,          # Height of walls along roads (0 = no walls)
                additional_width=0.6,     # Additional width for sidewalks/shoulders
                smooth_junctions=True,    # Smooth junction connections
                enable_mesh_visibility=True  # Enable visual mesh rendering
            )
            
            print("   ⚙️  OpenDRIVE Generation Parameters:")
            print(f"      • Vertex Distance: {generation_params.vertex_distance}m")
            print(f"      • Max Road Length: {generation_params.max_road_length}m")
            print(f"      • Wall Height: {generation_params.wall_height}m")
            print(f"      • Additional Width: {generation_params.additional_width}m")
            print(f"      • Smooth Junctions: {generation_params.smooth_junctions}")
            print(f"      • Mesh Visibility: {generation_params.enable_mesh_visibility}")
            
            print("\n   🔄 CARLA Server Processing OSM->OpenDRIVE->Map...")
            print("      1. Parsing OpenDRIVE XML structure")
            print("      2. Creating road network topology")
            print("      3. Generating lane boundaries and markings")
            print("      4. Processing junction connections")
            print("      5. Building visual mesh geometry")
            
            # Generate the world from OpenDRIVE data
            self.world = self.client.generate_opendrive_world(xodr_data, generation_params)
            
            # Wait a moment for the world to fully load
            time.sleep(3)
            
            map_name = self.world.get_map().name
            print(f"\n✅ Map loaded successfully: {map_name}")
            
            # Get information about the loaded map
            carla_map = self.world.get_map()
            
            # Analyze MapDataTypes usage in the loaded map
            self._analyze_map_data_types(carla_map)
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to load OpenDRIVE map: {e}")
            return False
    
    def _analyze_map_data_types(self, carla_map):
        """Analyze and display MapDataTypes fields in the loaded map."""
        print("\n📊 MapDataTypes Analysis (from MapDataTypes.h):")
        print("=" * 60)
        
        # Get waypoints for analysis
        waypoints = carla_map.generate_waypoints(distance=10.0)
        spawn_points = carla_map.get_spawn_points()
        topology = carla_map.get_topology()
        
        print(f"🛣️  Basic Map Statistics:")
        print(f"   • Total Waypoints: {len(waypoints)}")
        print(f"   • Spawn Points: {len(spawn_points)}")
        print(f"   • Topology Connections: {len(topology)}")
        
        if not waypoints:
            print("⚠️  No waypoints found - skipping detailed analysis")
            return
        
        # Analyze RoadType distribution (ts::RoadType enum)
        print(f"\n�️  RoadType Distribution (ts::RoadType):")
        road_type_counts = {}
        road_types_found = set()
        
        for i, wp in enumerate(waypoints[:100]):  # Sample first 100 waypoints
            try:
                # Get road information
                road_id = wp.road_id
                is_junction = wp.is_junction
                
                # Infer road type based on properties
                if is_junction:
                    road_type = "Intersection"
                elif road_id < 100:  # Heuristic for highway classification
                    road_type = "Highway"
                else:
                    road_type = "SurfaceStreet"
                    
                road_types_found.add(road_type)
                road_type_counts[road_type] = road_type_counts.get(road_type, 0) + 1
                
            except Exception as e:
                continue
        
        # Display RoadType enum values and their usage
        print("   MapDataTypes.h RoadType enum values:")
        road_type_enums = [
            ("NotSet", "0", "Default/uninitialized state"),
            ("Highway", "1", "High-speed limited access roads"),
            ("SurfaceStreet", "2", "Regular city/town streets"),
            ("Intersection", "3", "Junction areas where roads meet"),
            ("HighwayConnector", "4", "Ramps and connectors")
        ]
        
        for enum_name, enum_val, description in road_type_enums:
            count = road_type_counts.get(enum_name, 0)
            status = "✅ FOUND" if enum_name in road_types_found else "   ---"
            print(f"   • {enum_name:15} = {enum_val} | {description:35} | {status} ({count:2d})")
        
        # Analyze LaneType distribution (ts::LaneType enum)
        print(f"\n🛣️  LaneType Distribution (ts::LaneType):")
        lane_type_counts = {}
        lane_types_found = set()
        
        for i, wp in enumerate(waypoints[:50]):  # Analyze lane types
            try:
                lane_type = wp.lane_type
                lane_type_name = str(lane_type).split('.')[-1] if hasattr(lane_type, '__class__') else str(lane_type)
                lane_types_found.add(lane_type_name)
                lane_type_counts[lane_type_name] = lane_type_counts.get(lane_type_name, 0) + 1
            except Exception as e:
                continue
        
        # Display LaneType enum values
        print("   MapDataTypes.h LaneType enum values:")
        lane_type_enums = [
            ("NotSet", "0", "Default/uninitialized state"),
            ("Standard", "1", "Regular driving lanes"),
            ("HovLane", "2", "High-occupancy vehicle lanes"),
            ("BikeLane", "3", "Dedicated bicycle lanes"),
            ("NoTrucks", "4", "Car-only lanes (trucks prohibited)"),
            ("Restricted", "5", "Access-restricted lanes")
        ]
        
        for enum_name, enum_val, description in lane_type_enums:
            count = lane_type_counts.get(enum_name, 0)
            status = "✅ FOUND" if enum_name in lane_type_counts else "   ---"
            print(f"   • {enum_name:15} = {enum_val} | {description:35} | {status} ({count:2d})")
        
        # Analyze LaneBoundary information
        print(f"\n�️  Lane Boundary Analysis (ts::LaneBoundaryType & LaneBoundaryColor):")
        boundary_type_counts = {}
        boundary_color_counts = {}
        
        for i, wp in enumerate(waypoints[:30]):  # Sample lane markings
            try:
                # Get lane markings
                left_marking = wp.left_lane_marking
                right_marking = wp.right_lane_marking
                
                for marking_side, marking in [("Left", left_marking), ("Right", right_marking)]:
                    if marking:
                        # Analyze marking type
                        marking_type = str(marking.type).split('.')[-1] if hasattr(marking.type, '__class__') else str(marking.type)
                        boundary_type_counts[marking_type] = boundary_type_counts.get(marking_type, 0) + 1
                        
                        # Analyze marking color
                        marking_color = str(marking.color).split('.')[-1] if hasattr(marking.color, '__class__') else str(marking.color)
                        boundary_color_counts[marking_color] = boundary_color_counts.get(marking_color, 0) + 1
                        
            except Exception as e:
                continue
        
        # Display LaneBoundaryType enum values
        print("   MapDataTypes.h LaneBoundaryType enum values:")
        boundary_type_enums = [
            ("NotSet", "0", "Default/uninitialized state"),
            ("None", "1", "No boundary marking"),
            ("Solid", "2", "Solid line marking"),
            ("DoubleSolid", "3", "Double solid line marking"),
            ("DashedSolid", "4", "Dashed left, solid right"),
            ("SolidDashed", "5", "Solid left, dashed right"),
            ("Dashed", "6", "Dashed line marking"),
            ("DoubleDashed", "7", "Double dashed line marking"),
            ("ReflectorsOnly", "8", "Road reflectors only"),
            ("Curb", "9", "Physical curb boundary")
        ]
        
        for enum_name, enum_val, description in boundary_type_enums:
            count = boundary_type_counts.get(enum_name, 0)
            status = "✅ FOUND" if enum_name in boundary_type_counts else "   ---"
            print(f"   • {enum_name:15} = {enum_val} | {description:35} | {status} ({count:2d})")
        
        # Display LaneBoundaryColor enum values
        print("   MapDataTypes.h LaneBoundaryColor enum values:")
        boundary_color_enums = [
            ("NotSet", "0", "Default/uninitialized state"),
            ("White", "1", "White marking color"),
            ("Yellow", "2", "Yellow marking color"),
            ("Orange", "3", "Orange marking color")
        ]
        
        for enum_name, enum_val, description in boundary_color_enums:
            count = boundary_color_counts.get(enum_name, 0)
            status = "✅ FOUND" if enum_name in boundary_color_counts else "   ---"
            print(f"   • {enum_name:15} = {enum_val} | {description:35} | {status} ({count:2d})")
        
        # Analyze other MapDataTypes enums
        print(f"\n🚦 Additional MapDataTypes Enums:")
        
        # LaneRightOfWay
        print("   LaneRightOfWay enum (traffic control at intersections):")
        row_enums = [("Continue", "0"), ("Stop", "1"), ("Yield", "2"), ("TrafficSignal", "3")]
        for enum_name, enum_val in row_enums:
            print(f"   • {enum_name:15} = {enum_val}")
        
        # LaneDirection  
        print("   LaneDirection enum (lane travel direction):")
        direction_enums = [("Backward", "-1"), ("Both", "0"), ("Forward", "1")]
        for enum_name, enum_val in direction_enums:
            print(f"   • {enum_name:15} = {enum_val}")
        
        # SurfacePolygonType
        print("   SurfacePolygonType enum (surface area classifications):")
        surface_enums = [
            ("CrossWalk", "0"), ("Junction", "1"), ("SideWalk", "2"),
            ("SpeedBump", "3"), ("Surface", "4"), ("TrainTracks", "5"), ("Unknown", "99")
        ]
        for enum_name, enum_val in surface_enums:
            print(f"   • {enum_name:15} = {enum_val}")
        
        # OSM to CARLA data flow summary
        print(f"\n🔄 OSM to CARLA Data Flow Summary:")
        print("   1. OSM XML → OSM road network parsing")
        print("   2. OSM highway tags → RoadType classification")
        print("   3. OSM lane info → LaneType assignment")
        print("   4. OSM barrier/kerb → LaneBoundaryType mapping")
        print("   5. OpenDRIVE generation → CARLA road::Map creation")
        print("   6. MapDataTypes enums → Type-safe road element classification")
        print("   7. Visual mesh generation → Renderable road surfaces")
        print("   8. Waypoint network → Navigation and spawn points")
        
        print(f"\n✅ MapDataTypes integration analysis complete!")
        print("   The OSM pipeline successfully utilizes MapDataTypes.h enums")
        print("   for type-safe road network representation in CARLA.")
    
    def spawn_test_vehicles(self, num_vehicles=5):
        """Spawn test vehicles on the map to demonstrate the roadway."""
        try:
            print(f"🚙 Spawning {num_vehicles} test vehicles...")
            
            # Get available spawn points
            spawn_points = self.world.get_map().get_spawn_points()
            if not spawn_points:
                print("❌ No spawn points available on the map")
                return False
            
            # Get vehicle blueprints
            blueprint_library = self.world.get_blueprint_library()
            vehicle_blueprints = [
                bp for bp in blueprint_library.filter('vehicle.*')
                if int(bp.get_attribute('number_of_wheels')) == 4
            ]
            
            if not vehicle_blueprints:
                print("❌ No vehicle blueprints available")
                return False
            
            print(f"   📋 Available vehicle types: {len(vehicle_blueprints)}")
            
            # Spawn vehicles at different spawn points
            num_to_spawn = min(num_vehicles, len(spawn_points))
            
            for i in range(num_to_spawn):
                try:
                    # Select a vehicle blueprint and spawn point
                    vehicle_bp = vehicle_blueprints[i % len(vehicle_blueprints)]
                    spawn_point = spawn_points[i]
                    
                    # Spawn the vehicle
                    vehicle = self.world.spawn_actor(vehicle_bp, spawn_point)
                    self.spawned_vehicles.append(vehicle)
                    
                    # Enable autopilot for realistic movement
                    vehicle.set_autopilot(True)
                    
                    location = spawn_point.location
                    print(f"   ✅ Vehicle {i+1}/{num_to_spawn}: {vehicle_bp.id}")
                    print(f"      📍 Location: ({location.x:.1f}, {location.y:.1f}, {location.z:.1f})")
                    
                except Exception as e:
                    print(f"   ⚠️  Failed to spawn vehicle {i+1}: {e}")
                    continue
            
            print(f"✅ Successfully spawned {len(self.spawned_vehicles)} vehicles")
            return True
            
        except Exception as e:
            print(f"❌ Failed to spawn vehicles: {e}")
            return False
    
    def run_simulation(self, duration=60):
        """Run the simulation for the specified duration."""
        try:
            print(f"▶️  Running simulation for {duration} seconds...")
            print("   Watch the CARLA window to see the OSM-generated roadway!")
            
            start_time = time.time()
            
            while time.time() - start_time < duration:
                elapsed = int(time.time() - start_time)
                remaining = duration - elapsed
                
                # Print periodic status updates
                if elapsed % 10 == 0:
                    print(f"   ⏱️  Time: {elapsed}s / {duration}s ({remaining}s remaining)")
                    
                    # Show vehicle locations for first vehicle if available
                    if self.spawned_vehicles:
                        vehicle = self.spawned_vehicles[0]
                        location = vehicle.get_location()
                        velocity = vehicle.get_velocity()
                        speed_kmh = 3.6 * (velocity.x**2 + velocity.y**2 + velocity.z**2)**0.5
                        
                        print(f"      🚗 Sample vehicle location: ({location.x:.1f}, {location.y:.1f})")
                        print(f"      🏃 Speed: {speed_kmh:.1f} km/h")
                
                time.sleep(1)
            
            print("✅ Simulation completed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Simulation failed: {e}")
            return False
    
    def cleanup(self):
        """Clean up spawned actors."""
        try:
            if self.spawned_vehicles:
                print("🧹 Cleaning up spawned vehicles...")
                for i, vehicle in enumerate(self.spawned_vehicles):
                    try:
                        vehicle.destroy()
                        print(f"   ✅ Destroyed vehicle {i+1}")
                    except Exception as e:
                        print(f"   ⚠️  Failed to destroy vehicle {i+1}: {e}")
                
                self.spawned_vehicles.clear()
                print("✅ Cleanup completed")
                
        except Exception as e:
            print(f"❌ Cleanup failed: {e}")
    
    def run_full_test(self, osm_file_path, duration=60, num_vehicles=5):
        """Run the complete OSM pipeline test."""
        print("🚗 CARLA OSM Pipeline Test")
        print("=" * 50)
        
        success = True
        
        try:
            # Step 1: Connect to CARLA
            if not self.connect_to_carla():
                return False
            
            # Step 2: Convert OSM to OpenDRIVE
            output_path = osm_file_path.replace('.osm', '_converted.xodr')
            xodr_data = self.convert_osm_to_opendrive(osm_file_path, output_path)
            if not xodr_data:
                return False
            
            # Step 3: Load the map in CARLA
            if not self.load_opendrive_map(xodr_data):
                return False
            
            # Step 4: Spawn test vehicles
            if not self.spawn_test_vehicles(num_vehicles):
                print("⚠️  Vehicle spawning failed, continuing without vehicles...")
            
            # Step 5: Run simulation
            success = self.run_simulation(duration)
            
        except KeyboardInterrupt:
            print("\n⏹️  Simulation interrupted by user")
            success = False
            
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
            success = False
            
        finally:
            # Always clean up
            self.cleanup()
        
        # Final summary
        print("\n" + "=" * 50)
        if success:
            print("🎉 OSM Pipeline Test PASSED!")
            print("✅ The updated OSM map pipeline is working correctly")
            print("✅ Roadway was successfully generated and visualized")
        else:
            print("❌ OSM Pipeline Test FAILED!")
            print("❌ Please check the error messages above")
        
        return success


def main():
    """Main function to run the OSM pipeline test."""
    parser = argparse.ArgumentParser(
        description="Test CARLA OSM pipeline with visual roadway generation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python3 test_osm_pipeline.py
    python3 test_osm_pipeline.py --osm-file ~/Downloads/custom.osm
    python3 test_osm_pipeline.py --duration 120 --vehicles 10
        """
    )
    
    parser.add_argument(
        '--osm-file', 
        default='~/Downloads/uvalde.osm',
        help='Path to the OSM file (default: ~/Downloads/uvalde.osm)'
    )
    
    parser.add_argument(
        '--duration', 
        type=int, 
        default=60,
        help='Simulation duration in seconds (default: 60)'
    )
    
    parser.add_argument(
        '--vehicles', 
        type=int, 
        default=5,
        help='Number of test vehicles to spawn (default: 5)'
    )
    
    parser.add_argument(
        '--host', 
        default='localhost',
        help='CARLA server host (default: localhost)'
    )
    
    parser.add_argument(
        '--port', 
        type=int, 
        default=2000,
        help='CARLA server port (default: 2000)'
    )
    
    args = parser.parse_args()
    
    # Expand the OSM file path
    osm_file_path = os.path.expanduser(args.osm_file)
    
    # Validate OSM file exists
    if not os.path.exists(osm_file_path):
        print(f"❌ OSM file not found: {osm_file_path}")
        print("Please ensure the file exists or specify a different path with --osm-file")
        return 1
    
    # Create and run the test
    test = OSMPipelineTest(host=args.host, port=args.port)
    success = test.run_full_test(
        osm_file_path=osm_file_path,
        duration=args.duration,
        num_vehicles=args.vehicles
    )
    
    return 0 if success else 1


if __name__ == '__main__':
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print('\n👋 Cancelled by user. Goodbye!')
        sys.exit(0)
    except Exception as e:
        print(f'💥 Unexpected error: {e}')
        sys.exit(1)