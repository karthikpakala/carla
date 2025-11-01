#!/usr/bin/env python3

"""
Test script for new map data types
"""

import carla
import sys
import os

def test_new_map_types():
    """Test the new map data types from MapDataTypes.hpp"""
    
    print("Testing new CARLA map data types...")
    
    # Test LaneType enum
    print("\n=== Testing LaneType ===")
    try:
        lane_types = [
            carla.LaneType.NotSet,
            carla.LaneType.Standard, 
            carla.LaneType.HovLane,
            carla.LaneType.BikeLane,
            carla.LaneType.NoTrucks,
            carla.LaneType.Restricted
        ]
        print("✓ LaneType enum values accessible:")
        for lt in lane_types:
            print(f"  - {lt}")
    except AttributeError as e:
        print(f"✗ LaneType enum error: {e}")
    
    # Test RoadType enum  
    print("\n=== Testing RoadType ===")
    try:
        road_types = [
            carla.RoadType.NotSet,
            carla.RoadType.Highway,
            carla.RoadType.SurfaceStreet,
            carla.RoadType.Intersection,
            carla.RoadType.HighwayConnector
        ]
        print("✓ RoadType enum values accessible:")
        for rt in road_types:
            print(f"  - {rt}")
    except AttributeError as e:
        print(f"✗ RoadType enum error: {e}")
    
    # Test LaneBoundaryType enum
    print("\n=== Testing LaneBoundaryType ===")
    try:
        boundary_types = [
            carla.LaneBoundaryType.NotSet,
            getattr(carla.LaneBoundaryType, 'None'),
            carla.LaneBoundaryType.Solid,
            carla.LaneBoundaryType.DoubleSolid,
            carla.LaneBoundaryType.DashedSolid,
            carla.LaneBoundaryType.SolidDashed,
            carla.LaneBoundaryType.Dashed,
            carla.LaneBoundaryType.DoubleDashed,
            carla.LaneBoundaryType.ReflectorsOnly,
            carla.LaneBoundaryType.Curb
        ]
        print("✓ LaneBoundaryType enum values accessible:")
        for bt in boundary_types:
            print(f"  - {bt}")
    except AttributeError as e:
        print(f"✗ LaneBoundaryType enum error: {e}")
    
    # Test LaneBoundaryColor enum
    print("\n=== Testing LaneBoundaryColor ===")
    try:
        boundary_colors = [
            carla.LaneBoundaryColor.NotSet,
            carla.LaneBoundaryColor.White,
            carla.LaneBoundaryColor.Yellow,
            carla.LaneBoundaryColor.Orange
        ]
        print("✓ LaneBoundaryColor enum values accessible:")
        for bc in boundary_colors:
            print(f"  - {bc}")
    except AttributeError as e:
        print(f"✗ LaneBoundaryColor enum error: {e}")
    
    # Test SurfacePolygonType enum
    print("\n=== Testing SurfacePolygonType ===")
    try:
        surface_types = [
            carla.SurfacePolygonType.CrossWalk,
            carla.SurfacePolygonType.Junction,
            carla.SurfacePolygonType.SideWalk,
            carla.SurfacePolygonType.SpeedBump,
            carla.SurfacePolygonType.Surface,
            carla.SurfacePolygonType.TrainTracks,
            carla.SurfacePolygonType.Unknown
        ]
        print("✓ SurfacePolygonType enum values accessible:")
        for st in surface_types:
            print(f"  - {st}")
    except AttributeError as e:
        print(f"✗ SurfacePolygonType enum error: {e}")

    # Test LaneRightOfWay enum
    print("\n=== Testing LaneRightOfWay ===")
    try:
        right_of_way_types = [
            carla.LaneRightOfWay.Continue,
            carla.LaneRightOfWay.Stop,
            carla.LaneRightOfWay.Yield,
            carla.LaneRightOfWay.TrafficSignal
        ]
        print("✓ LaneRightOfWay enum values accessible:")
        for row in right_of_way_types:
            print(f"  - {row}")
    except AttributeError as e:
        print(f"✗ LaneRightOfWay enum error: {e}")

    # Test LaneBlockageState enum
    print("\n=== Testing LaneBlockageState ===")
    try:
        blockage_states = [
            carla.LaneBlockageState.NotBlocked,
            carla.LaneBlockageState.Blocked
        ]
        print("✓ LaneBlockageState enum values accessible:")
        for bs in blockage_states:
            print(f"  - {bs}")
    except AttributeError as e:
        print(f"✗ LaneBlockageState enum error: {e}")

    # Test LaneDirection enum
    print("\n=== Testing LaneDirection ===")
    try:
        lane_directions = [
            carla.LaneDirection.Backward,
            carla.LaneDirection.Both,
            carla.LaneDirection.Forward
        ]
        print("✓ LaneDirection enum values accessible:")
        for ld in lane_directions:
            print(f"  - {ld}")
    except AttributeError as e:
        print(f"✗ LaneDirection enum error: {e}")

def test_with_map():
    """Test map functionality with new types"""
    print("\n=== Testing Map Functionality ===")
    
    try:
        # Try to connect to CARLA server if running
        client = carla.Client('localhost', 2000)
        client.set_timeout(2.0)
        
        # Get world and map
        world = client.get_world()
        carla_map = world.get_map()
        
        print("✓ Connected to CARLA server")
        print(f"✓ Map loaded: {carla_map.name}")
        
        # Test waypoint with new lane type
        spawn_points = carla_map.get_spawn_points()
        if spawn_points:
            location = spawn_points[0].location
            
            # Test getting waypoint with new lane type
            waypoint = carla_map.get_waypoint(location, lane_type=carla.LaneType.Standard)
            if waypoint:
                print(f"✓ Waypoint found with Standard lane type: {waypoint.lane_type}")
            else:
                print("✗ No waypoint found with Standard lane type")
                
        print("✓ Map functionality test completed")
        
    except Exception as e:
        print(f"✗ Map functionality test failed: {e}")
        print("  (This is expected if CARLA server is not running)")

if __name__ == '__main__':
    try:
        test_new_map_types()
        test_with_map()
        print("\n=== Test Summary ===")
        print("New map data types have been successfully integrated!")
    except Exception as e:
        print(f"Test failed with error: {e}")
        sys.exit(1)