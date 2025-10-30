#!/usr/bin/env python

"""
Simple OSM Map Loader for CARLA

This is a simplified version that just loads an OSM map into CARLA without running a full scenario.

Usage:
    python simple_osm_loader.py --osm-path ~/Downloads/semantic-62077.osm
"""

import glob
import os
import sys
import argparse

# CARLA Python API should be installed via pip
# If not installed, use: pip install PythonAPI/carla/dist/carla-*.whl

import carla

def main():
    parser = argparse.ArgumentParser(description='Simple OSM Map Loader')
    parser.add_argument(
        '--osm-path',
        required=True,
        help='Path to the OSM file to load'
    )
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
    
    args = parser.parse_args()
    
    try:
        # Connect to CARLA
        print(f"Connecting to CARLA server at {args.host}:{args.port}")
        client = carla.Client(args.host, args.port)
        client.set_timeout(30.0)
        
        # Test connection
        world = client.get_world()
        print("Successfully connected to CARLA server")
        
        # Load OSM file
        print(f"Loading OSM file: {args.osm_path}")
        
        if not os.path.exists(args.osm_path):
            print(f"OSM file not found: {args.osm_path}")
            return
        
        # Read the OSM file
        with open(args.osm_path, 'r', encoding='utf-8') as osm_file:
            osm_data = osm_file.read()
        
        print("Converting OSM to OpenDRIVE...")
        
        # Configure conversion settings
        settings = carla.Osm2OdrSettings()
        settings.set_osm_way_types([
            "motorway", "motorway_link",
            "trunk", "trunk_link", 
            "primary", "primary_link",
            "secondary", "secondary_link", 
            "tertiary", "tertiary_link",
            "unclassified", "residential"
        ])
        
        # Convert to OpenDRIVE
        xodr_data = carla.Osm2Odr.convert(osm_data, settings)
        
        print("Loading map into CARLA...")
        
        # Generate the world
        world = client.generate_opendrive_world(
            xodr_data, 
            carla.OpendriveGenerationParameters(
                vertex_distance=2.0,
                max_road_length=500.0,
                wall_height=0.0,
                additional_width=0.6,
                smooth_junctions=True,
                enable_mesh_visibility=True
            )
        )
        
        print("OSM map successfully loaded!")
        print("You can now manually control vehicles or run other scenarios.")
        print("Map spawn points:", len(world.get_map().get_spawn_points()))
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()