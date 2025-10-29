// Copyright (c) 2025 Computer Vision Center (CVC) at the Universitat Autonoma
// de Barcelona (UAB).
//
// This work is licensed under the terms of the MIT license.
// For a copy, see <https://opensource.org/licenses/MIT>.

#pragma once

#include "carla/road/RoadTypes.h"
#include "carla/road/Lane.h"
#include "carla/road/element/LaneMarking.h"

namespace carla {
namespace road {

/// Utility class for converting between OSM map data types and CARLA types
class OSMMapDataConverter {
public:
  /// Convert OSM highway types to CARLA lane types
  static Lane::LaneType ConvertOSMWayTypeToLaneType(const std::string& osm_way_type);
  
  /// Convert TS lane type to CARLA lane type
  static Lane::LaneType ConvertTSLaneTypeToCarlaLaneType(ts::LaneType ts_type);
  
  /// Convert TS road type to CARLA road type
  static ts::RoadType ConvertTSRoadTypeToCarlaRoadType(ts::RoadType ts_type);
  
  /// Convert TS boundary type to CARLA lane marking
  static element::LaneMarking::Type ConvertTSBoundaryTypeToLaneMarking(ts::LaneBoundaryType ts_boundary);
  
  /// Convert TS boundary color to CARLA lane marking color
  static element::LaneMarking::Color ConvertTSBoundaryColorToLaneMarkingColor(ts::LaneBoundaryColor ts_color);
  
  /// Convert lane direction to navigation info
  static bool ConvertLaneDirectionToNavigable(ts::LaneDirection direction);
  
  /// Convert TS surface polygon type to appropriate lane type
  static Lane::LaneType ConvertSurfacePolygonTypeToLaneType(ts::SurfacePolygonType surface_type);

private:
  /// Private constructor to prevent instantiation
  OSMMapDataConverter() = delete;
};

} // namespace road
} // namespace carla