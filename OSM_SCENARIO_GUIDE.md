# CARLA OSM Map Scenario Guide

This guide explains how to run scenarios using CARLA with your OSM map file located at `~/Downloads/semantic-62077.osm`.

## What We've Set Up

I've created several scripts to help you work with OSM maps in CARLA:

### 1. `simple_osm_loader.py` - Basic OSM Map Loader
This script loads an OSM map into CARLA without running a full scenario.

**Usage:**
```bash
python3 simple_osm_loader.py --osm-path ~/Downloads/semantic-62077.osm
```

### 2. `osm_scenario.py` - Full OSM Scenario Runner
This script loads an OSM map and runs a complete scenario with vehicles and sensors.

**Usage:**
```bash
python3 osm_scenario.py --osm-path ~/Downloads/semantic-62077.osm --duration 60 --num-npc 5
```

### 3. `basic_carla_scenario.py` - Built-in Map Scenario
This script runs scenarios with CARLA's built-in maps (good for testing).

**Usage:**
```bash
python3 basic_carla_scenario.py --duration 30 --num-npc 5
```

### 4. `load_osm_map.sh` - Shell Script Using CARLA's Built-in Tools
This uses CARLA's existing `config.py` utility.

**Usage:**
```bash
./load_osm_map.sh ~/Downloads/semantic-62077.osm
```

## Prerequisites

1. **CARLA Server Running:**
   ```bash
   cd /home/karthik.pakala@torc.ai/carla/Dist/CARLA_Shipping_965899a78-dirty/LinuxNoEditor
   ./CarlaUE4.sh -carla-world-port=2000
   ```

2. **CARLA Python API Installed:**
   ```bash
   pip install /home/karthik.pakala@torc.ai/carla/PythonAPI/carla/dist/carla-0.9.16-cp313-cp313-linux_x86_64.whl --force-reinstall
   ```

## Issues We Encountered

### Large Map Size
Your OSM file (`semantic-62077.osm`) is very large (391MB), which causes:
- Long conversion times (OSM → OpenDRIVE)
- Memory and timeout issues when loading into CARLA
- Warning: "Network contains very large coordinates"

### Solutions and Recommendations

#### Option 1: Use a Smaller OSM Area
For better performance, consider using a smaller area from OpenStreetMap:

1. Go to [OpenStreetMap](https://www.openstreetmap.org)
2. Navigate to your desired location
3. Click "Export" and select a smaller area (1-2 km²)
4. Use this smaller OSM file with our scripts

#### Option 2: CARLA's Built-in Maps for Testing
Start with CARLA's built-in maps to test the scenario functionality:

```bash
# List available maps
python3 -c "
import carla
client = carla.Client('127.0.0.1', 2000)
client.set_timeout(10.0)
print('Available maps:')
for map_name in client.get_available_maps():
    print(' -', map_name)
"

# Run scenario with a specific map
python3 basic_carla_scenario.py --map Town03 --duration 30
```

#### Option 3: Use CARLA's Config Utility
The most reliable method for OSM loading:

```bash
cd /home/karthik.pakala@torc.ai/carla/PythonAPI/util
python3 config.py --osm-path="/home/karthik.pakala@torc.ai/Downloads/semantic-62077.osm"
```

## What the Scripts Do

### OSM Conversion Process
1. **Read OSM File:** Parse the XML-formatted OSM data
2. **Configure Settings:** Set road types, lane widths, traffic lights
3. **Convert to OpenDRIVE:** Use `carla.Osm2Odr.convert()`
4. **Generate CARLA World:** Create 3D world from OpenDRIVE data

### Scenario Features
- **Ego Vehicle:** Main vehicle (player controlled or autopilot)
- **NPC Vehicles:** AI-controlled traffic vehicles
- **Sensors:** Camera, LIDAR, GPS (configurable)
- **Data Recording:** Save sensor data to files
- **Synchronous Mode:** Consistent simulation timing

## Example Workflow

1. **Start CARLA Server:**
   ```bash
   cd /home/karthik.pakala@torc.ai/carla/Dist/CARLA_Shipping_965899a78-dirty/LinuxNoEditor
   ./CarlaUE4.sh -carla-world-port=2000
   ```

2. **Test Basic Scenario (Built-in Map):**
   ```bash
   cd /home/karthik.pakala@torc.ai/carla
   python3 basic_carla_scenario.py --duration 20
   ```

3. **Try OSM Loading (if map is small enough):**
   ```bash
   python3 simple_osm_loader.py --osm-path ~/Downloads/semantic-62077.osm
   ```

4. **View Sensor Data:**
   ```bash
   ls -la ./sensor_data/
   ```

## Troubleshooting

### Connection Issues
- Ensure CARLA server is running: `pgrep -f CarlaUE4`
- Check port availability: `netstat -tlnp | grep 2000`
- Increase timeout in scripts if needed

### Memory/Performance Issues
- Use smaller OSM areas
- Reduce number of NPC vehicles
- Lower image resolution for sensors
- Use asynchronous mode for better performance

### Map Loading Timeouts
- The large OSM file may need very long timeouts
- Consider splitting large areas into smaller segments
- Use CARLA's tile streaming for large maps

## Next Steps

1. **Get CARLA running stable** with built-in maps first
2. **Test with a smaller OSM area** (1-2 km²)
3. **Gradually increase map complexity** as system handles it
4. **Customize scenarios** based on your specific needs

Let me know if you need help with any specific part of this workflow!