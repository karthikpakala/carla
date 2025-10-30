#!/bin/bash

# OSM Map Loader Script for CARLA
# This script uses CARLA's built-in config.py utility to load OSM maps

# Usage: ./load_osm_map.sh /path/to/your/map.osm

if [ $# -eq 0 ]; then
    echo "Usage: $0 <path_to_osm_file>"
    echo "Example: $0 ~/Downloads/semantic-62077.osm"
    exit 1
fi

OSM_FILE="$1"

# Check if the OSM file exists
if [ ! -f "$OSM_FILE" ]; then
    echo "Error: OSM file not found: $OSM_FILE"
    exit 1
fi

echo "Loading OSM map: $OSM_FILE"
echo "Make sure CARLA server is running..."

# Change to the CARLA PythonAPI util directory
cd /home/karthik.pakala@torc.ai/carla/PythonAPI/util

# Load the OSM map using config.py
python3 config.py --osm-path="$OSM_FILE"

echo "OSM map loading completed!"
echo "You can now connect with a client and spawn vehicles."