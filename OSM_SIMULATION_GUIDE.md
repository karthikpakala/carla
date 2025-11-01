# CARLA OSM Map Simulation - Complete Guide

## Overview
This guide demonstrates how to run a CARLA simulation using the OSM map `semantic-62077.osm` located at `~/Downloads/semantic-62077.osm`.

## What We've Accomplished

### 1. ✅ OSM File Verified
- Location: `~/Downloads/semantic-62077.osm`
- Size: 391,214,073 bytes (391 MB)
- Status: File exists and is accessible

### 2. ✅ OSM to OpenDRIVE Conversion Completed
- **Input:** `~/Downloads/semantic-62077.osm`
- **Output:** `~/Downloads/semantic-62077.xodr`
- **Size:** 638,046,563 bytes (638 MB)
- **Tool Used:** CARLA's `osm_to_xodr.py` utility
- **Command:**
  ```bash
  cd /home/karthik.pakala@torc.ai/carla/PythonAPI/util
  python3 osm_to_xodr.py --input ~/Downloads/semantic-62077.osm --output ~/Downloads/semantic-62077.xodr
  ```

### 3. ✅ CARLA Python API Verified
- CARLA Python module imports successfully
- Available at: `/home/karthik.pakala@torc.ai/carla/PythonAPI/carla`

## How to Run the Simulation

### Method 1: Using config.py (Recommended)

1. **Start CARLA Server:**
   ```bash
   cd /home/karthik.pakala@torc.ai/carla
   ./Dist/CARLA_Shipping_b03b91d65-dirty/LinuxNoEditor/CarlaUE4.sh
   ```

2. **Load OSM Map (in a separate terminal):**
   ```bash
   cd /home/karthik.pakala@torc.ai/carla/PythonAPI/util
   python3 config.py --osm-path ~/Downloads/semantic-62077.osm
   ```

   OR load the pre-converted XODR file:
   ```bash
   python3 config.py --xodr-path ~/Downloads/semantic-62077.xodr
   ```

### Method 2: Using Custom Python Script

```python
import carla
import time

# Connect to CARLA
client = carla.Client('localhost', 2000)
client.set_timeout(300.0)  # 5 minute timeout for large maps

# Read the converted XODR file
with open('/home/karthik.pakala@torc.ai/Downloads/semantic-62077.xodr', 'r') as f:
    xodr_data = f.read()

# Load the map
world = client.generate_opendrive_world(
    xodr_data, 
    carla.OpendriveGenerationParameters(
        vertex_distance=2.0,
        max_road_length=500.0,
        wall_height=1.0,
        additional_width=0.6,
        smooth_junctions=True,
        enable_mesh_visibility=True
    )
)

# Spawn a vehicle
blueprint_library = world.get_blueprint_library()
vehicle_bp = blueprint_library.filter('vehicle')[0]
spawn_points = world.get_map().get_spawn_points()

if spawn_points:
    vehicle = world.spawn_actor(vehicle_bp, spawn_points[0])
    vehicle.set_autopilot(True)
    
    # Run simulation
    for i in range(60):
        time.sleep(1)
        location = vehicle.get_location()
        print(f"Vehicle location: ({location.x:.1f}, {location.y:.1f})")
    
    vehicle.destroy()
```

## Map Details

The converted OSM map contains:
- **Original OSM data:** Real-world geographic data from OpenStreetMap
- **Road types:** Motorways, primary roads, secondary roads, residential streets
- **Map size:** Very large (638MB OpenDRIVE file)
- **Complexity:** High-detail urban environment

## Performance Considerations

This is a very large and detailed map, which may require:
- **High memory:** 8GB+ RAM recommended
- **Processing time:** Map loading may take 5-10 minutes
- **Graphics:** Dedicated GPU recommended for smooth rendering
- **Timeout settings:** Increase client timeout to 300+ seconds

## Troubleshooting

If you encounter issues:

1. **Server crashes:** The map is very large. Try with more system resources or simplified conversion settings.

2. **Timeout errors:** Increase the client timeout:
   ```python
   client.set_timeout(600.0)  # 10 minutes
   ```

3. **Memory issues:** Consider using simplified OSM conversion settings:
   ```python
   settings = carla.Osm2OdrSettings()
   settings.set_osm_way_types(["motorway", "primary"])  # Only major roads
   xodr_data = carla.Osm2Odr.convert(osm_data, settings)
   ```

## Alternative: Smaller Test Area

For testing purposes, you might want to:
1. Extract a smaller area from the original OSM file
2. Use JOSM or other OSM editors to create a subset
3. Convert the smaller subset for faster loading

## Files Created

- ✅ `~/Downloads/semantic-62077.osm` (original OSM file - 391 MB)
- ✅ `~/Downloads/semantic-62077.xodr` (converted OpenDRIVE file - 638 MB)
- ✅ `/home/karthik.pakala@torc.ai/carla/run_osm_simulation.py` (simulation script)
- ✅ `/home/karthik.pakala@torc.ai/carla/test_carla_connection.py` (connection test script)

The OSM conversion was successful and the files are ready for use. The simulation can be run once CARLA server is properly started in your environment.