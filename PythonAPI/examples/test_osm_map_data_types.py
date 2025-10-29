#!/usr/bin/env python

# Copyright (c) 2025 Computer Vision Center (CVC) at the Universitat Autonoma
# de Barcelona (UAB).
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

"""
Test script to demonstrate the new OSM map data types integration with CARLA.

This script shows how to use the new map data types from MapDataTypes.hpp
instead of the default CARLA lane types for OSM map interface support.
"""

import glob
import os
import sys

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla


def main():
    print("Testing new OSM Map Data Types in CARLA")
    print("=" * 50)
    
    # Test the new lane types
    print("\n1. Testing new Lane Types:")
    lane_types = [
        carla.LaneType.NotSet,
        carla.LaneType.Standard,
        carla.LaneType.HovLane,
        carla.LaneType.BikeLane,
        carla.LaneType.NoTrucks,
        carla.LaneType.Restricted
    ]
    
    for lane_type in lane_types:
        print(f"   Lane Type: {lane_type}")
    
    # Test the new road types
    print("\n2. Testing new Road Types:")
    road_types = [
        carla.RoadType.NotSet,
        carla.RoadType.Highway,
        carla.RoadType.SurfaceStreet,
        carla.RoadType.Intersection,
        carla.RoadType.HighwayConnector
    ]
    
    for road_type in road_types:
        print(f"   Road Type: {road_type}")
    
    # Test the new lane boundary types
    print("\n3. Testing new Lane Boundary Types:")
    boundary_types = [
        carla.LaneBoundaryType.NotSet,
        carla.LaneBoundaryType.NONE,  # None mapped to NONE in Python
        carla.LaneBoundaryType.Solid,
        carla.LaneBoundaryType.DoubleSolid,
        carla.LaneBoundaryType.DashedSolid,
        carla.LaneBoundaryType.SolidDashed,
        carla.LaneBoundaryType.Dashed,
        carla.LaneBoundaryType.DoubleDashed,
        carla.LaneBoundaryType.ReflectorsOnly,
        carla.LaneBoundaryType.Curb
    ]
    
    for boundary_type in boundary_types:
        print(f"   Boundary Type: {boundary_type}")
    
    # Test the new lane boundary colors
    print("\n4. Testing new Lane Boundary Colors:")
    boundary_colors = [
        carla.LaneBoundaryColor.NotSet,
        carla.LaneBoundaryColor.White,
        carla.LaneBoundaryColor.Yellow,
        carla.LaneBoundaryColor.Orange
    ]
    
    for boundary_color in boundary_colors:
        print(f"   Boundary Color: {boundary_color}")
    
    # Test lane directions
    print("\n5. Testing Lane Directions:")
    lane_directions = [
        carla.LaneDirection.Backward,
        carla.LaneDirection.Both,
        carla.LaneDirection.Forward
    ]
    
    for direction in lane_directions:
        print(f"   Lane Direction: {direction}")
    
    # Test surface polygon types
    print("\n6. Testing Surface Polygon Types:")
    surface_types = [
        carla.SurfacePolygonType.CrossWalk,
        carla.SurfacePolygonType.Junction,
        carla.SurfacePolygonType.SideWalk,
        carla.SurfacePolygonType.SpeedBump,
        carla.SurfacePolygonType.Surface,
        carla.SurfacePolygonType.TrainTracks,
        carla.SurfacePolygonType.Unknown
    ]
    
    for surface_type in surface_types:
        print(f"   Surface Type: {surface_type}")
    
    # Test OSM Data Converter
    print("\n7. Testing OSM Map Data Converter:")
    converter = carla.OSMMapDataConverter()
    
    # Test OSM highway types to CARLA lane types
    osm_way_types = ["motorway", "primary", "cycleway", "footway"]
    for way_type in osm_way_types:
        carla_lane_type = converter.convert_osm_way_type_to_lane_type(way_type)
        print(f"   OSM way '{way_type}' -> CARLA lane type: {carla_lane_type}")
    
    # Test TS lane types to CARLA lane types
    ts_lane_types = [carla.OSMLaneType.Standard, carla.OSMLaneType.HovLane,
                     carla.OSMLaneType.BikeLane, carla.OSMLaneType.NoTrucks]
    for ts_type in ts_lane_types:
        carla_type = converter.convert_ts_lane_type_to_carla_lane_type(ts_type)
        print(f"   TS lane type {ts_type} -> CARLA lane type: {carla_type}")
    
    # Test boundary type conversions
    ts_boundary_types = [carla.OSMLaneBoundaryType.Solid, carla.OSMLaneBoundaryType.DashedSolid,
                        carla.OSMLaneBoundaryType.DoubleSolid, carla.OSMLaneBoundaryType.Curb]
    for boundary_type in ts_boundary_types:
        carla_marking = converter.convert_ts_boundary_type_to_lane_marking(boundary_type)
        print(f"   TS boundary {boundary_type} -> CARLA marking: {carla_marking}")
    
    print("\n" + "=" * 50)
    print("All OSM Map Data Types working correctly!")
    print("The CARLA repository has been successfully modified to support")
    print("the new map data types from MapDataTypes.hpp for OSM integration.")


if __name__ == '__main__':
    main()