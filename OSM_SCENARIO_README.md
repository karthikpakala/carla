# CARLA OSM Scenario Scripts

This directory contains Python scripts for creating and running scenarios using OpenStreetMap (OSM) files in CARLA.

## Scripts Overview

### 1. `osm_scenario_runner.py` - Complete Scenario Runner
A comprehensive script with full functionality for OSM-based scenarios.

**Features:**
- ✅ OSM to OpenDRIVE conversion
- ✅ Map loading in CARLA
- ✅ Vehicle spawning with autopilot
- ✅ Pedestrian spawning with AI
- ✅ Weather control
- ✅ Sensor data collection
- ✅ Configurable parameters
- ✅ Graceful cleanup

### 2. `quick_osm_test.py` - Simple Test Script
A lightweight script for quick testing and validation.

**Features:**
- ✅ Basic OSM loading test
- ✅ Single vehicle spawn
- ✅ 30-second simulation
- ✅ Performance optimized

## Prerequisites

### 1. CARLA Server Running
Make sure CARLA server is running before executing the scripts:

```bash
cd /home/karthik.pakala@torc.ai/carla/Dist/CARLA_Shipping_b03b91d65-dirty/LinuxNoEditor
./CarlaUE4.sh
```

### 2. OSM File
The scripts expect the OSM file at: `~/Downloads/semantic-62077.osm`

Current file status:
- ✅ File exists: `~/Downloads/semantic-62077.osm`
- ✅ Size: 391.2 MB
- ✅ Ready for use

## Usage

### Quick Test (Recommended First Step)

```bash
cd /home/karthik.pakala@torc.ai/carla
python3 quick_osm_test.py
```

This will:
1. Check OSM file availability
2. Connect to CARLA server
3. Convert OSM to OpenDRIVE (simplified)
4. Load the map
5. Spawn one test vehicle
6. Run for 30 seconds
7. Clean up

### Full Scenario Runner

#### Basic Usage
```bash
python3 osm_scenario_runner.py
```

#### Advanced Usage with Parameters
```bash
python3 osm_scenario_runner.py \
    --osm-file ~/Downloads/semantic-62077.osm \
    --vehicles 15 \
    --pedestrians 25 \
    --duration 600 \
    --weather storm \
    --simplified \
    --save-sensors
```

#### Available Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--osm-file` | `~/Downloads/semantic-62077.osm` | Path to OSM file |
| `--host` | `localhost` | CARLA server host |
| `--port` | `2000` | CARLA server port |
| `--vehicles` | `10` | Number of vehicles to spawn |
| `--pedestrians` | `20` | Number of pedestrians to spawn |
| `--duration` | `300` | Scenario duration (seconds) |
| `--weather` | `clear` | Weather preset |
| `--simplified` | `False` | Use simplified conversion |
| `--save-sensors` | `False` | Save sensor data |

#### Weather Options
- `clear` - Clear sunny day
- `cloudy` - Cloudy conditions  
- `wet` - Wet roads
- `storm` - Heavy rain
- `sunset` - Sunset lighting
- `night` - Night conditions
- `random` - Random weather

## Expected Output

### Quick Test Output
```
🚗 Quick OSM Scenario Test
========================================
✅ OSM file found: 391.2 MB

📡 Connecting to CARLA...
✅ Connected! Current map: Town10HD_Opt

📄 Reading OSM file...
✅ OSM data loaded: 391,214,073 characters

🔄 Converting OSM to OpenDRIVE (simplified)...
✅ Conversion successful: 45,678,912 characters

🗺️  Loading map in CARLA...
✅ Map loaded: OpenDrive_0_1698765432

✅ Found 1,234 spawn points

🚙 Spawning test vehicle...
✅ Vehicle spawned: vehicle.tesla.model3
   Location: (123.4, 567.8)
✅ Autopilot enabled

⏱️  Running simulation for 30 seconds...
  Time:  1s | Location: ( 123.4,  567.8) | Speed:   0.0 km/h
  Time:  6s | Location: ( 125.2,  568.1) | Speed:  12.3 km/h
  Time: 11s | Location: ( 128.7,  569.4) | Speed:  25.6 km/h
  ...

🧹 Cleaning up...
✅ Vehicle destroyed

🎉 Test completed successfully!
```

### Full Scenario Runner Output
```
🚗 CARLA OSM Scenario Runner
==================================================

=== Converting OSM to OpenDRIVE ===
OSM data loaded: 391,214,073 characters
Using simplified conversion settings for better performance...
Converting OSM to OpenDRIVE... (this may take several minutes)
✓ Conversion successful! OpenDRIVE size: 45,678,912 characters
✓ Saved OpenDRIVE to: /home/.../semantic-62077_converted.xodr

=== Loading Map in CARLA ===
Loading OpenDRIVE world (45,678,912 characters)...
✓ Map loaded successfully!
✓ New world: OpenDrive_0_1698765432

=== Setting Weather: clear ===
✓ Weather set successfully

=== Spawning 10 Vehicles ===
Available vehicle types: 45
Found 1,234 spawn points
  ✓ Vehicle 1/10: vehicle.tesla.model3
  ✓ Vehicle 2/10: vehicle.bmw.grandtourer
  ...
✓ Successfully spawned 10 vehicles

=== Spawning 20 Pedestrians ===
Available pedestrian types: 15
  ✓ Pedestrian 1/18: walker.pedestrian.0001
  ✓ Pedestrian 2/18: walker.pedestrian.0002
  ...
✓ Successfully spawned 18 pedestrians

=== Running Scenario for 300 seconds ===
⏱️  Simulation time: 0s / 300s
   📍 Vehicle location: (123.4, 567.8)
   🚗 Vehicle speed: 0.0 km/h
⏱️  Simulation time: 10s / 300s
   📍 Vehicle location: (134.7, 572.1)
   🚗 Vehicle speed: 32.5 km/h
...
✓ Scenario completed successfully!

=== Cleaning Up ===
✓ Destroyed 10 vehicles
✓ Destroyed 36 pedestrians
✓ Cleanup completed
```

## Performance Considerations

### System Requirements
- **RAM:** 8GB+ recommended (OSM map is 391MB, converted to 638MB+ XODR)
- **GPU:** Dedicated GPU recommended for smooth rendering
- **CPU:** Multi-core processor for traffic simulation
- **Storage:** 2GB+ free space for temporary files

### Optimization Tips

1. **Use Simplified Mode:**
   ```bash
   python3 osm_scenario_runner.py --simplified
   ```

2. **Reduce Actor Count:**
   ```bash
   python3 osm_scenario_runner.py --vehicles 5 --pedestrians 10
   ```

3. **Shorter Duration:**
   ```bash
   python3 osm_scenario_runner.py --duration 120
   ```

## Troubleshooting

### Common Issues

1. **"CARLA server not running"**
   - Start CARLA server first
   - Check host/port parameters
   - Verify server is accessible

2. **"OSM file not found"**
   - Verify file exists at `~/Downloads/semantic-62077.osm`
   - Use `--osm-file` parameter to specify different path

3. **"Conversion takes too long"**
   - Use `--simplified` flag
   - The 391MB OSM file is very large - conversion may take 5-10 minutes

4. **"Map loading fails"**
   - Increase CARLA server timeout
   - Check system memory (needs 8GB+)
   - Try simplified conversion

5. **"No spawn points available"**
   - Map conversion may have failed
   - Try different OSM file or conversion settings

### Debug Mode
For detailed error information, modify the scripts to include:
```python
import traceback
# ... in exception handlers:
traceback.print_exc()
```

## Files Created During Execution

The scripts will create these files:
- `~/Downloads/semantic-62077_converted.xodr` - Converted OpenDRIVE map
- `sensor_data/` directory (if `--save-sensors` is used)
  - `camera_*.png` - Camera images
  - `lidar_*.ply` - LiDAR point clouds

## Integration with Existing Scripts

These scripts complement the existing CARLA setup:
- `test_new_map_types.py` - Tests new map data types
- `run_osm_simulation.py` - Original OSM simulation script
- `test_carla_connection.py` - Connection testing

## Next Steps

1. **Start with Quick Test:** Run `quick_osm_test.py` first
2. **Gradual Scaling:** Start with fewer vehicles/pedestrians
3. **Performance Monitoring:** Watch system resources during execution
4. **Custom Scenarios:** Modify scripts for specific use cases

## Support

For issues or questions:
1. Check the console output for specific error messages
2. Verify CARLA server is running and accessible
3. Ensure OSM file is valid and accessible
4. Monitor system resources (RAM, CPU, GPU)