// Copyright (c) 2025 Computer Vision Center (CVC) at the Universitat Autonoma
// de Barcelona (UAB).
//
// This work is licensed under the terms of the MIT license.
// For a copy, see <https://opensource.org/licenses/MIT>.

#include "carla/road/OSMMapDataConverter.h"
#include <unordered_map>
#include <string>

namespace carla {
namespace road {

Lane::LaneType OSMMapDataConverter::ConvertOSMWayTypeToLaneType(const std::string& osm_way_type) {
  // Map common OSM highway tags to TS lane types
  static const std::unordered_map<std::string, Lane::LaneType> osm_to_ts_lane_types = {
    {"motorway", ts::LaneType::Standard},
    {"trunk", ts::LaneType::Standard},
    {"primary", ts::LaneType::Standard},
    {"secondary", ts::LaneType::Standard},
    {"tertiary", ts::LaneType::Standard},
    {"residential", ts::LaneType::Standard},
    {"service", ts::LaneType::Restricted},
    {"track", ts::LaneType::Restricted},
    {"cycleway", ts::LaneType::BikeLane},
    {"footway", ts::LaneType::Restricted},
    {"path", ts::LaneType::Restricted},
    {"pedestrian", ts::LaneType::Restricted},
    {"living_street", ts::LaneType::Standard},
    {"unclassified", ts::LaneType::Standard},
    {"bus_guideway", ts::LaneType::HovLane},
    {"escape", ts::LaneType::Restricted},
    {"raceway", ts::LaneType::Standard}
  };
  
  auto it = osm_to_ts_lane_types.find(osm_way_type);
  return (it != osm_to_ts_lane_types.end()) ? it->second : ts::LaneType::Standard;
}

Lane::LaneType OSMMapDataConverter::ConvertTSLaneTypeToCarlaLaneType(ts::LaneType ts_type) {
  // Direct mapping since we're using ts types as the new carla types
  return ts_type;
}

ts::RoadType OSMMapDataConverter::ConvertTSRoadTypeToCarlaRoadType(ts::RoadType ts_type) {
  // Direct mapping since we're using ts types as the new carla types
  return ts_type;
}

element::LaneMarking::Type OSMMapDataConverter::ConvertTSBoundaryTypeToLaneMarking(ts::LaneBoundaryType ts_boundary) {
  switch (ts_boundary) {
    case ts::LaneBoundaryType::None:
      return element::LaneMarking::Type::None;
    case ts::LaneBoundaryType::Solid:
      return element::LaneMarking::Type::Solid;
    case ts::LaneBoundaryType::DoubleSolid:
      return element::LaneMarking::Type::SolidSolid;
    case ts::LaneBoundaryType::DashedSolid:
      return element::LaneMarking::Type::BrokenSolid;
    case ts::LaneBoundaryType::SolidDashed:
      return element::LaneMarking::Type::SolidBroken;
    case ts::LaneBoundaryType::Dashed:
      return element::LaneMarking::Type::Broken;
    case ts::LaneBoundaryType::DoubleDashed:
      return element::LaneMarking::Type::BrokenBroken;
    case ts::LaneBoundaryType::ReflectorsOnly:
      return element::LaneMarking::Type::BottsDots;
    case ts::LaneBoundaryType::Curb:
      return element::LaneMarking::Type::Curb;
    case ts::LaneBoundaryType::NotSet:
    default:
      return element::LaneMarking::Type::Other;
  }
}

element::LaneMarking::Color OSMMapDataConverter::ConvertTSBoundaryColorToLaneMarkingColor(ts::LaneBoundaryColor ts_color) {
  switch (ts_color) {
    case ts::LaneBoundaryColor::White:
      return element::LaneMarking::Color::White;
    case ts::LaneBoundaryColor::Yellow:
      return element::LaneMarking::Color::Yellow;
    case ts::LaneBoundaryColor::Orange:
      return element::LaneMarking::Color::Other; // Map orange to other since not directly supported
    case ts::LaneBoundaryColor::NotSet:
    default:
      return element::LaneMarking::Color::Standard;
  }
}

bool OSMMapDataConverter::ConvertLaneDirectionToNavigable(ts::LaneDirection direction) {
  switch (direction) {
    case ts::LaneDirection::Forward:
    case ts::LaneDirection::Both:
      return true;
    case ts::LaneDirection::Backward:
    default:
      return false;
  }
}

Lane::LaneType OSMMapDataConverter::ConvertSurfacePolygonTypeToLaneType(ts::SurfacePolygonType surface_type) {
  switch (surface_type) {
    case ts::SurfacePolygonType::CrossWalk:
      return ts::LaneType::Restricted; // Pedestrian area
    case ts::SurfacePolygonType::Junction:
      return ts::LaneType::Standard; // Intersection driving area
    case ts::SurfacePolygonType::SideWalk:
      return ts::LaneType::Restricted; // Non-drivable pedestrian area
    case ts::SurfacePolygonType::SpeedBump:
      return ts::LaneType::Standard; // Still drivable but with speed restriction
    case ts::SurfacePolygonType::Surface:
      return ts::LaneType::Standard; // General drivable surface
    case ts::SurfacePolygonType::TrainTracks:
      return ts::LaneType::Restricted; // Not for general vehicles
    case ts::SurfacePolygonType::Unknown:
    default:
      return ts::LaneType::Standard; // Default to standard when unknown
  }
}

} // namespace road
} // namespace carla