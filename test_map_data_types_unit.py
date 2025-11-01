#!/usr/bin/env python3

"""
Unit tests for new map data types integration
"""

import unittest
import sys
import os

# Add CARLA Python API to path
sys.path.append('/home/karthik.pakala@torc.ai/carla/PythonAPI/carla/dist/carla-*-py3.*-linux-x86_64.egg')

try:
    import carla
except ImportError:
    print("CARLA Python API not found. Please build CARLA first.")
    sys.exit(1)

class TestNewMapDataTypes(unittest.TestCase):
    """Test suite for new map data types from MapDataTypes.hpp"""
    
    def test_lane_type_enum(self):
        """Test LaneType enum values"""
        # Test all new lane types are accessible
        self.assertTrue(hasattr(carla, 'LaneType'))
        
        # Test specific values
        self.assertTrue(hasattr(carla.LaneType, 'NotSet'))
        self.assertTrue(hasattr(carla.LaneType, 'Standard'))
        self.assertTrue(hasattr(carla.LaneType, 'HovLane'))
        self.assertTrue(hasattr(carla.LaneType, 'BikeLane'))
        self.assertTrue(hasattr(carla.LaneType, 'NoTrucks'))
        self.assertTrue(hasattr(carla.LaneType, 'Restricted'))
        
        # Test values are different
        self.assertNotEqual(carla.LaneType.NotSet, carla.LaneType.Standard)
        self.assertNotEqual(carla.LaneType.Standard, carla.LaneType.HovLane)
    
    def test_road_type_enum(self):
        """Test RoadType enum values"""
        # Test all road types are accessible
        self.assertTrue(hasattr(carla, 'RoadType'))
        
        # Test specific values
        self.assertTrue(hasattr(carla.RoadType, 'NotSet'))
        self.assertTrue(hasattr(carla.RoadType, 'Highway'))
        self.assertTrue(hasattr(carla.RoadType, 'SurfaceStreet'))
        self.assertTrue(hasattr(carla.RoadType, 'Intersection'))
        self.assertTrue(hasattr(carla.RoadType, 'HighwayConnector'))
        
        # Test values are different
        self.assertNotEqual(carla.RoadType.NotSet, carla.RoadType.Highway)
        self.assertNotEqual(carla.RoadType.Highway, carla.RoadType.SurfaceStreet)
    
    def test_lane_boundary_type_enum(self):
        """Test LaneBoundaryType enum values"""
        # Test all boundary types are accessible
        self.assertTrue(hasattr(carla, 'LaneBoundaryType'))
        
        # Test specific values
        self.assertTrue(hasattr(carla.LaneBoundaryType, 'NotSet'))
        self.assertTrue(hasattr(carla.LaneBoundaryType, 'None'))
        self.assertTrue(hasattr(carla.LaneBoundaryType, 'Solid'))
        self.assertTrue(hasattr(carla.LaneBoundaryType, 'DoubleSolid'))
        self.assertTrue(hasattr(carla.LaneBoundaryType, 'DashedSolid'))
        self.assertTrue(hasattr(carla.LaneBoundaryType, 'SolidDashed'))
        self.assertTrue(hasattr(carla.LaneBoundaryType, 'Dashed'))
        self.assertTrue(hasattr(carla.LaneBoundaryType, 'DoubleDashed'))
        self.assertTrue(hasattr(carla.LaneBoundaryType, 'ReflectorsOnly'))
        self.assertTrue(hasattr(carla.LaneBoundaryType, 'Curb'))
    
    def test_lane_boundary_color_enum(self):
        """Test LaneBoundaryColor enum values"""
        # Test all boundary colors are accessible
        self.assertTrue(hasattr(carla, 'LaneBoundaryColor'))
        
        # Test specific values
        self.assertTrue(hasattr(carla.LaneBoundaryColor, 'NotSet'))
        self.assertTrue(hasattr(carla.LaneBoundaryColor, 'White'))
        self.assertTrue(hasattr(carla.LaneBoundaryColor, 'Yellow'))
        self.assertTrue(hasattr(carla.LaneBoundaryColor, 'Orange'))
    
    def test_surface_polygon_type_enum(self):
        """Test SurfacePolygonType enum values"""
        # Test all surface polygon types are accessible
        self.assertTrue(hasattr(carla, 'SurfacePolygonType'))
        
        # Test specific values
        self.assertTrue(hasattr(carla.SurfacePolygonType, 'CrossWalk'))
        self.assertTrue(hasattr(carla.SurfacePolygonType, 'Junction'))
        self.assertTrue(hasattr(carla.SurfacePolygonType, 'SideWalk'))
        self.assertTrue(hasattr(carla.SurfacePolygonType, 'SpeedBump'))
        self.assertTrue(hasattr(carla.SurfacePolygonType, 'Surface'))
        self.assertTrue(hasattr(carla.SurfacePolygonType, 'TrainTracks'))
        self.assertTrue(hasattr(carla.SurfacePolygonType, 'Unknown'))
    
    def test_lane_right_of_way_enum(self):
        """Test LaneRightOfWay enum values"""
        # Test all right of way types are accessible
        self.assertTrue(hasattr(carla, 'LaneRightOfWay'))
        
        # Test specific values
        self.assertTrue(hasattr(carla.LaneRightOfWay, 'Continue'))
        self.assertTrue(hasattr(carla.LaneRightOfWay, 'Stop'))
        self.assertTrue(hasattr(carla.LaneRightOfWay, 'Yield'))
        self.assertTrue(hasattr(carla.LaneRightOfWay, 'TrafficSignal'))
    
    def test_lane_blockage_state_enum(self):
        """Test LaneBlockageState enum values"""
        # Test all blockage states are accessible
        self.assertTrue(hasattr(carla, 'LaneBlockageState'))
        
        # Test specific values
        self.assertTrue(hasattr(carla.LaneBlockageState, 'NotBlocked'))
        self.assertTrue(hasattr(carla.LaneBlockageState, 'Blocked'))
    
    def test_lane_direction_enum(self):
        """Test LaneDirection enum values"""
        # Test all lane directions are accessible
        self.assertTrue(hasattr(carla, 'LaneDirection'))
        
        # Test specific values
        self.assertTrue(hasattr(carla.LaneDirection, 'Backward'))
        self.assertTrue(hasattr(carla.LaneDirection, 'Both'))
        self.assertTrue(hasattr(carla.LaneDirection, 'Forward'))
    
    def test_enum_values_are_integers(self):
        """Test that enum values are integers (for compatibility)"""
        # Test a few representative values
        self.assertIsInstance(int(carla.LaneType.Standard), int)
        self.assertIsInstance(int(carla.RoadType.Highway), int) 
        self.assertIsInstance(int(carla.LaneBoundaryType.Solid), int)
        self.assertIsInstance(int(carla.LaneBoundaryColor.White), int)

class TestMapIntegration(unittest.TestCase):
    """Test integration with CARLA map functionality"""
    
    def setUp(self):
        """Set up test client if CARLA server is running"""
        try:
            self.client = carla.Client('localhost', 2000)
            self.client.set_timeout(2.0)
            self.world = self.client.get_world()
            self.carla_map = self.world.get_map()
            self.server_available = True
        except:
            self.server_available = False
            
    def test_waypoint_lane_type(self):
        """Test waypoint lane type with new enum"""
        if not self.server_available:
            self.skipTest("CARLA server not available")
            
        # Get a waypoint
        spawn_points = self.carla_map.get_spawn_points()
        self.assertGreater(len(spawn_points), 0, "No spawn points available")
        
        waypoint = self.carla_map.get_waypoint(
            spawn_points[0].location, 
            lane_type=carla.LaneType.Standard
        )
        
        self.assertIsNotNone(waypoint, "Could not get waypoint with Standard lane type")
        
        # Test that the lane type is accessible
        lane_type = waypoint.lane_type
        self.assertIsNotNone(lane_type, "Waypoint lane type is None")
    
    def test_junction_waypoints_with_new_types(self):
        """Test junction waypoints with new lane types"""
        if not self.server_available:
            self.skipTest("CARLA server not available")
            
        # Get topology to find junctions
        topology = self.carla_map.get_topology()
        self.assertGreater(len(topology), 0, "No topology available")
        
        # Find a junction
        for start_waypoint, end_waypoint in topology:
            if start_waypoint.is_junction:
                junction = start_waypoint.get_junction()
                self.assertIsNotNone(junction, "Could not get junction")
                
                # Test getting waypoints with new lane type
                junction_waypoints = junction.get_waypoints(carla.LaneType.Standard)
                # This should not raise an exception
                break

class TestOSMCompatibility(unittest.TestCase):
    """Test OSM file compatibility"""
    
    def test_osm_file_exists(self):
        """Test that the semantic OSM file exists"""
        osm_file_path = os.path.expanduser("~/Downloads/semantic-62077.osm")
        
        if os.path.exists(osm_file_path):
            self.assertTrue(True, f"OSM file found at {osm_file_path}")
            
            # Check file size
            file_size = os.path.getsize(osm_file_path)
            self.assertGreater(file_size, 0, "OSM file is empty")
            
            print(f"OSM file size: {file_size / 1024:.1f} KB")
        else:
            self.skipTest(f"OSM file not found at {osm_file_path}")

if __name__ == '__main__':
    # Run the test suite
    unittest.main(verbosity=2)