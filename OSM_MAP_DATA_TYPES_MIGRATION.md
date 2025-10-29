# CARLA OSM Map Data Types Migration

## Overview

This document describes the comprehensive changes made to the CARLA repository to replace the default lane and road data types with the new OSM-compatible data types from `MapDataTypes.hpp`. This migration removes support for the old data types completely and implements full support for OSM map interfaces.

## Changes Made

### 1. Core Data Types Migration

#### Lane.h
- **File**: `LibCarla/source/carla/road/Lane.h`
- **Changes**:
  - Replaced the existing `LaneType` enum with `ts::LaneType` from `MapDataTypes.hpp`
  - Added type aliases for all new OSM data types:
    - `LaneType = ts::LaneType`
    - `RoadType = ts::RoadType`
    - `LaneBoundaryType = ts::LaneBoundaryType`
    - `LaneBoundaryColor = ts::LaneBoundaryColor`
    - `LaneBlockageState = ts::LaneBlockageState`
    - `LaneDirection = ts::LaneDirection`
    - `LaneRightOfWay = ts::LaneRightOfWay`
    - `SurfacePolygonType = ts::SurfacePolygonType`
  - Changed default lane type from `LaneType::None` to `LaneType::NotSet`

### 2. OSM Data Converter Implementation

#### OSMMapDataConverter.h & OSMMapDataConverter.cpp
- **Files**: 
  - `LibCarla/source/carla/road/OSMMapDataConverter.h`
  - `LibCarla/source/carla/road/OSMMapDataConverter.cpp`
- **Changes**:
  - Implemented comprehensive conversion functions between OSM/TS types and CARLA types
  - Added mapping for common OSM highway tags to lane types
  - Implemented boundary type and color conversions
  - Added surface polygon type to lane type mapping

### 3. Python API Bindings

#### Map.cpp
- **File**: `PythonAPI/carla/source/libcarla/Map.cpp`
- **Changes**:
  - Replaced old `LaneType` enum with new `ts::LaneType` values
  - Added all new OSM data type enums:
    - `RoadType`, `LaneBoundaryType`, `LaneBoundaryColor`
    - `LaneBlockageState`, `LaneDirection`, `LaneRightOfWay`, `SurfacePolygonType`
  - Updated default lane type parameter in `GetWaypoint` method

#### OSMMapDataTypes.cpp
- **File**: `PythonAPI/carla/source/libcarla/OSMMapDataTypes.cpp`
- **Changes**:
  - Created comprehensive Python bindings for all OSM data types
  - Added `OSMMapDataConverter` class bindings with all conversion methods
  - Handled Python keyword conflicts (e.g., `None` → `NONE`)

#### libcarla.cpp
- **File**: `PythonAPI/carla/source/libcarla/libcarla.cpp`
- **Changes**:
  - Added export for `export_osm_map_data_types()` function

### 4. Parsing Logic Updates

#### RoadParser.cpp
- **File**: `LibCarla/source/carla/opendrive/parser/RoadParser.cpp`
- **Changes**:
  - Updated `StringToLaneType` function to map OpenDRIVE lane types to new TS types
  - Mapped legacy types to appropriate new types:
    - `driving` → `ts::LaneType::Standard`
    - `biking` → `ts::LaneType::BikeLane`
    - `restricted` → `ts::LaneType::Restricted`
    - etc.

### 5. Map Building Logic

#### MapBuilder.cpp
- **File**: `LibCarla/source/carla/road/MapBuilder.cpp`
- **Changes**:
  - Updated all lane type references from old enum values to new TS types
  - Changed `Lane::LaneType::Driving` → `ts::LaneType::Standard`
  - Changed `Lane::LaneType::None` → `ts::LaneType::NotSet`
  - Updated junction waypoint logic and signal positioning

### 6. Rendering System

#### MeshFactory.cpp
- **File**: `LibCarla/source/carla/road/MeshFactory.cpp`
- **Changes**:
  - Updated all switch statements to use new lane types
  - Remapped rendering logic:
    - `Standard`, `HovLane`, `NoTrucks` → tessellated rendering
    - `BikeLane`, `Restricted` → sidewalk rendering
  - Updated material assignments to use new type checks

### 7. Unreal Engine Integration

#### CarlaGameModeBase.cpp
- **File**: `Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Game/CarlaGameModeBase.cpp`
- **Changes**:
  - Simplified lane type to boundary type mapping
  - Consolidated old 20+ lane types into 5 new TS types
  - Updated `AssignBoundaryType` lambda function

#### OpenDriveToMap.cpp
- **File**: `Unreal/CarlaUE4/Plugins/CarlaTools/Source/CarlaTools/Private/OpenDriveToMap.cpp`
- **Changes**:
  - Updated `LaneTypeToFString` function
  - Replaced all old lane type cases with new TS type cases
  - Simplified from 20+ types to 5 new types

### 8. Lane Marking System

#### LaneMarking.h
- **File**: `LibCarla/source/carla/road/element/LaneMarking.h`
- **Changes**:
  - Added type aliases for new boundary types from `MapDataTypes.hpp`
  - Integrated `ts::LaneBoundaryType` and `ts::LaneBoundaryColor`

### 9. Test Implementation

#### test_osm_map_data_types.py
- **File**: `PythonAPI/examples/test_osm_map_data_types.py`
- **Changes**:
  - Created comprehensive test script demonstrating all new data types
  - Tests all OSM data type enums and conversion functions
  - Handles Python keyword conflicts appropriately

## New OSM Data Types Supported

### Lane Types
- `NotSet` - Unspecified lane type
- `Standard` - Regular driving lane (replaces old Driving, Parking, etc.)
- `HovLane` - High-occupancy vehicle lane
- `BikeLane` - Dedicated bicycle lane
- `NoTrucks` - Lane restricted from trucks
- `Restricted` - General restricted lane (replaces Shoulder, Sidewalk, etc.)

### Road Types
- `NotSet` - Unspecified road type
- `Highway` - Highway/motorway
- `SurfaceStreet` - Surface street
- `Intersection` - Intersection area
- `HighwayConnector` - Highway connector/ramp

### Lane Boundary Types
- `NotSet` - Unspecified boundary
- `None` - No boundary marking
- `Solid` - Solid line
- `DoubleSolid` - Double solid line
- `DashedSolid` - Dashed left, solid right
- `SolidDashed` - Solid left, dashed right
- `Dashed` - Dashed line
- `DoubleDashed` - Double dashed line
- `ReflectorsOnly` - Reflectors/Botts' dots
- `Curb` - Physical curb

### Additional Types
- **Lane Boundary Colors**: `NotSet`, `White`, `Yellow`, `Orange`
- **Lane Directions**: `Backward`, `Both`, `Forward`
- **Lane Right of Way**: `Continue`, `Stop`, `Yield`, `TrafficSignal`
- **Surface Polygon Types**: `CrossWalk`, `Junction`, `SideWalk`, `SpeedBump`, `Surface`, `TrainTracks`, `Unknown`

## Backwards Compatibility

**IMPORTANT**: This migration completely removes support for the old data types. The following old lane types are no longer supported:

- `Driving`, `Stop`, `Shoulder`, `Biking`, `Sidewalk`, `Border`
- `Parking`, `Bidirectional`, `Median`, `Special1`, `Special2`, `Special3`
- `RoadWorks`, `Tram`, `Rail`, `Entry`, `Exit`, `OffRamp`, `OnRamp`, `Any`

These have been consolidated into the 5 new OSM-compatible types listed above.

## Usage Examples

### Python API
```python
import carla

# Use new lane types
lane_type = carla.LaneType.Standard
boundary_type = carla.LaneBoundaryType.Solid
boundary_color = carla.LaneBoundaryColor.Yellow

# Convert OSM data
converter = carla.OSMMapDataConverter()
carla_type = converter.convert_osm_way_type_to_lane_type("motorway")
```

### C++
```cpp
#include "carla/road/MapDataTypes.hpp"
#include "carla/road/OSMMapDataConverter.h"

// Use new types
ts::LaneType lane_type = ts::LaneType::Standard;
ts::RoadType road_type = ts::RoadType::Highway;

// Convert OSM data
auto carla_type = OSMMapDataConverter::ConvertOSMWayTypeToLaneType("cycleway");
```

## Testing

Run the provided test script to verify all changes:
```bash
cd PythonAPI/examples
python test_osm_map_data_types.py
```

This migration provides full OSM map interface support while maintaining CARLA's existing functionality with the new, more standardized data types.