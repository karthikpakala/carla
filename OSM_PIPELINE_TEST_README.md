# OSM Pipeline Test Scripts

This directory contains test scripts to validate the updated OSM (OpenStreetMap) map pipeline in CARLA. These scripts demonstrate the ability to convert OSM files to OpenDRIVE format and load them as drivable roadways in CARLA.

## Test Scripts Overview

### 1. `test_osm_pipeline.py` - Complete Pipeline Test
A comprehensive test script that demonstrates the full OSM pipeline functionality.

**Features:**
- ✅ OSM to OpenDRIVE conversion with configurable settings
- ✅ Map loading in CARLA with visual mesh generation
- ✅ Multiple vehicle spawning with autopilot
- ✅ Real-time simulation monitoring
- ✅ Detailed progress reporting
- ✅ Automatic cleanup
- ✅ Command-line configuration options

### 2. `quick_osm_test.py` - Quick Validation Test
A lightweight script for rapid pipeline validation.

**Features:**
- ✅ Basic OSM file validation
- ✅ Simple conversion test
- ✅ Single vehicle spawn test
- ✅ 30-second simulation
- ✅ Essential functionality check

## Prerequisites

### 1. CARLA Server Running
Make sure CARLA server is running before executing the scripts:

```bash
# Navigate to your CARLA installation directory
cd /home/karthik.pakala@torc.ai/carla/Dist/CARLA_Shipping_*/LinuxNoEditor
./CarlaUE4.sh
```

### 2. OSM File Available
The scripts expect an OSM file at: `~/Downloads/uvalde.osm`

Current file status:
- ✅ File exists: `~/Downloads/uvalde.osm`
- ✅ Size: ~594 KB
- ✅ Ready for testing

### 3. Python Environment
Ensure you have Python 3.6+ with the CARLA Python API available.

## Usage

### MapDataTypes Integration Demo (Start Here!)

Run the MapDataTypes integration demo first to understand the data flow:

```bash
cd /home/karthik.pakala@torc.ai/carla
python3 osm_mapdatatypes_demo.py
```

This demonstrates how OSM data flows through MapDataTypes.h enums during processing.

### Quick Test

Run the quick test to validate basic functionality:

```bash
cd /home/karthik.pakala@torc.ai/carla
python3 quick_osm_test.py
```

**Expected Output:**
```
🚗 Quick OSM Pipeline Test
========================================
✅ OSM file found: 594.1 KB

📡 Connecting to CARLA...
✅ Connected! Current map: Town10HD_Opt

📄 Reading OSM file...
✅ OSM data loaded: 609,007 characters

🔄 Converting OSM to OpenDRIVE (simplified)...
✅ Conversion successful: 1,234,567 characters

🗺️  Loading map in CARLA...
✅ Map loaded: OpenDrive_0_1730419200

✅ Found 45 spawn points

🚙 Spawning test vehicle...
✅ Vehicle spawned: vehicle.tesla.model3
   📍 Location: (123.4, 567.8)
✅ Autopilot enabled

⏱️  Running simulation for 30 seconds...
  Time:  5s | Location: ( 123.4,  567.8) | Speed:   0.0 km/h
  Time: 10s | Location: ( 125.2,  568.1) | Speed:  12.3 km/h
  Time: 15s | Location: ( 128.7,  569.4) | Speed:  25.6 km/h
  Time: 20s | Location: ( 132.1,  570.8) | Speed:  28.9 km/h
  Time: 25s | Location: ( 135.6,  572.2) | Speed:  30.1 km/h
  Time: 30s | Location: ( 139.0,  573.5) | Speed:  31.2 km/h

🧹 Cleaning up...
✅ Vehicle destroyed

🎉 Test completed successfully!
✅ The OSM pipeline is working correctly!
```

### Full Pipeline Test

For comprehensive testing with more vehicles and longer simulation:

```bash
# Basic usage
python3 test_osm_pipeline.py

# With custom parameters
python3 test_osm_pipeline.py --duration 120 --vehicles 10

# With different OSM file
python3 test_osm_pipeline.py --osm-file ~/Downloads/custom.osm --vehicles 8 --duration 180
```

**Command Line Options:**

| Option | Default | Description |
|--------|---------|-------------|
| `--osm-file` | `~/Downloads/uvalde.osm` | Path to OSM file |
| `--duration` | `60` | Simulation duration (seconds) |
| `--vehicles` | `5` | Number of test vehicles |
| `--host` | `localhost` | CARLA server host |
| `--port` | `2000` | CARLA server port |

**Expected Output:**
```
🚗 CARLA OSM Pipeline Test
==================================================

🔌 Connecting to CARLA server at localhost:2000...
✅ Successfully connected to CARLA server!
📍 Current map: Town10HD_Opt

📄 Reading OSM file: /home/.../Downloads/uvalde.osm
✅ OSM data loaded: 609,007 characters (0.6 MB)

⚙️  Configuring conversion settings...
🔄 Converting OSM to OpenDRIVE format...
   This may take a moment for larger OSM files...
✅ Conversion successful: 1,987,654 characters (1.9 MB)
💾 Saved OpenDRIVE file: /home/.../Downloads/uvalde_converted.xodr

🗺️  Loading OpenDRIVE map in CARLA...
✅ Map loaded successfully: OpenDrive_0_1730419200

📊 Map Statistics:
   🚗 Spawn points: 67
   🛣️  Waypoints: 2,435
   🔗 Topology connections: 234

🚙 Spawning 5 test vehicles...
   📋 Available vehicle types: 45
   ✅ Vehicle 1/5: vehicle.tesla.model3
      📍 Location: (123.4, 567.8, 0.3)
   ✅ Vehicle 2/5: vehicle.bmw.grandtourer
      📍 Location: (234.5, 678.9, 0.3)
   ✅ Vehicle 3/5: vehicle.ford.mustang
      📍 Location: (345.6, 789.0, 0.3)
   ✅ Vehicle 4/5: vehicle.toyota.prius
      📍 Location: (456.7, 890.1, 0.3)
   ✅ Vehicle 5/5: vehicle.mercedes.coupe
      📍 Location: (567.8, 901.2, 0.3)
✅ Successfully spawned 5 vehicles

▶️  Running simulation for 60 seconds...
   Watch the CARLA window to see the OSM-generated roadway!
   ⏱️  Time: 0s / 60s (60s remaining)
      🚗 Sample vehicle location: (123.4, 567.8)
      🏃 Speed: 0.0 km/h
   ⏱️  Time: 10s / 60s (50s remaining)
      🚗 Sample vehicle location: (145.2, 572.1)
      🏃 Speed: 25.3 km/h
   ...
✅ Simulation completed successfully!

🧹 Cleaning up spawned vehicles...
   ✅ Destroyed vehicle 1
   ✅ Destroyed vehicle 2
   ✅ Destroyed vehicle 3
   ✅ Destroyed vehicle 4
   ✅ Destroyed vehicle 5
✅ Cleanup completed

==================================================
🎉 OSM Pipeline Test PASSED!
✅ The updated OSM map pipeline is working correctly
✅ Roadway was successfully generated and visualized
```

## What to Look for in CARLA

When running these tests, watch the CARLA simulator window. You should see:

1. **Map Loading:** The view will change as the new OSM-based map loads
2. **Road Network:** Streets and intersections from the uvalde.osm file
3. **Vehicle Movement:** Test vehicles driving autonomously on the generated roads
4. **Road Features:** Lane markings, intersections, and road geometry from the OSM data

## Generated Files

The scripts create these files during execution:

- `~/Downloads/uvalde_converted.xodr` - The converted OpenDRIVE map file
- Console output with detailed progress and statistics

## Troubleshooting

### Common Issues

1. **"CARLA server not running"**
   ```
   ❌ Failed to connect to CARLA server: [Errno 111] Connection refused
   ```
   **Solution:** Start the CARLA server first:
   ```bash
   cd /path/to/carla/Dist/CARLA_Shipping_*/LinuxNoEditor
   ./CarlaUE4.sh
   ```

2. **"OSM file not found"**
   ```
   ❌ OSM file not found: /home/.../Downloads/uvalde.osm
   ```
   **Solution:** Verify the file exists or specify a different path:
   ```bash
   python3 test_osm_pipeline.py --osm-file /path/to/your/file.osm
   ```

3. **"Conversion takes too long"**
   - The uvalde.osm file is relatively small and should convert quickly
   - For larger OSM files, conversion may take several minutes
   - Monitor console output for progress updates

4. **"No spawn points available"**
   ```
   ❌ No spawn points available on the map
   ```
   **Solution:** The OSM conversion may have failed or the map lacks drivable roads
   - Check that the OSM file contains road data
   - Try the quick test first to validate basic functionality

5. **"Import carla could not be resolved"**
   - This is a linting error and can be ignored
   - The scripts correctly add the CARLA Python API to the path at runtime

### Performance Tips

1. **Start Small:** Use the quick test first to validate functionality
2. **Monitor Resources:** Large OSM files require significant RAM during conversion
3. **Reduce Vehicles:** Start with fewer vehicles and increase gradually
4. **Check Console:** Watch for specific error messages and warnings

## OSM File Requirements

The test scripts work with standard OSM files that contain:
- Road network data (`highway` tags)
- Basic road classifications (primary, secondary, residential, etc.)
- Junction/intersection information

The included `uvalde.osm` file contains a sample road network suitable for testing.

## Integration with CARLA Development

These test scripts demonstrate:
- **New Map Data Types:** Enhanced lane boundary types and road classifications
- **OSM Compatibility:** Improved OSM to OpenDRIVE conversion pipeline
- **Visual Generation:** Real-time road network visualization in CARLA
- **Automated Testing:** Validation scripts for continuous integration

## Next Steps

1. **Start with Quick Test:** Run `quick_osm_test.py` to validate basic functionality
2. **Full Pipeline Test:** Use `test_osm_pipeline.py` for comprehensive validation
3. **Custom OSM Files:** Test with your own OSM data files
4. **Parameter Tuning:** Experiment with different conversion settings
5. **Integration:** Incorporate into your CARLA development workflow

## Support and Development

These scripts are part of the updated CARLA OSM pipeline development. For issues:

1. Check console output for specific error messages
2. Verify CARLA server is running and accessible  
3. Ensure OSM file contains valid road network data
4. Monitor system resources during conversion and simulation

The scripts provide detailed error reporting to help diagnose issues and validate the OSM pipeline functionality.