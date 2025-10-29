// Copyright (c) 2025 Computer Vision Center (CVC) at the Universitat Autonoma
// de Barcelona (UAB).
//
// This work is licensed under the terms of the MIT license.
// For a copy, see <https://opensource.org/licenses/MIT>.

#include <carla/road/MapDataTypes.hpp>
#include <carla/road/OSMMapDataConverter.h>

void export_osm_map_data_types() {
  using namespace boost::python;
  namespace ts = ::ts;
  namespace crod = carla::road;

  // ===========================================================================
  // -- OSM Map Data Types -----------------------------------------------------
  // ===========================================================================

  enum_<ts::RoadType>("OSMRoadType")
    .value("NotSet", ts::RoadType::NotSet)
    .value("Highway", ts::RoadType::Highway)
    .value("SurfaceStreet", ts::RoadType::SurfaceStreet)
    .value("Intersection", ts::RoadType::Intersection)
    .value("HighwayConnector", ts::RoadType::HighwayConnector)
  ;

  enum_<ts::LaneBoundaryType>("OSMLaneBoundaryType")
    .value("NotSet", ts::LaneBoundaryType::NotSet)
    .value("NONE", ts::LaneBoundaryType::None) // None is reserved in Python3
    .value("Solid", ts::LaneBoundaryType::Solid)
    .value("DoubleSolid", ts::LaneBoundaryType::DoubleSolid)
    .value("DashedSolid", ts::LaneBoundaryType::DashedSolid)
    .value("SolidDashed", ts::LaneBoundaryType::SolidDashed)
    .value("Dashed", ts::LaneBoundaryType::Dashed)
    .value("DoubleDashed", ts::LaneBoundaryType::DoubleDashed)
    .value("ReflectorsOnly", ts::LaneBoundaryType::ReflectorsOnly)
    .value("Curb", ts::LaneBoundaryType::Curb)
  ;

  enum_<ts::LaneType>("OSMLaneType")
    .value("NotSet", ts::LaneType::NotSet)
    .value("Standard", ts::LaneType::Standard)
    .value("HovLane", ts::LaneType::HovLane)
    .value("BikeLane", ts::LaneType::BikeLane)
    .value("NoTrucks", ts::LaneType::NoTrucks)
    .value("Restricted", ts::LaneType::Restricted)
  ;

  enum_<ts::LaneRightOfWay>("OSMLaneRightOfWay")
    .value("Continue", ts::LaneRightOfWay::Continue)
    .value("Stop", ts::LaneRightOfWay::Stop)
    .value("Yield", ts::LaneRightOfWay::Yield)
    .value("TrafficSignal", ts::LaneRightOfWay::TrafficSignal)
  ;

  enum_<ts::LaneBoundaryColor>("OSMLaneBoundaryColor")
    .value("NotSet", ts::LaneBoundaryColor::NotSet)
    .value("White", ts::LaneBoundaryColor::White)
    .value("Yellow", ts::LaneBoundaryColor::Yellow)
    .value("Orange", ts::LaneBoundaryColor::Orange)
  ;

  enum_<ts::LaneBlockageState>("OSMLaneBlockageState")
    .value("NotBlocked", ts::LaneBlockageState::NotBlocked)
    .value("Blocked", ts::LaneBlockageState::Blocked)
  ;

  enum_<ts::LaneDirection>("OSMLaneDirection")
    .value("Backward", ts::LaneDirection::Backward)
    .value("Both", ts::LaneDirection::Both)
    .value("Forward", ts::LaneDirection::Forward)
  ;

  enum_<ts::SurfacePolygonType>("OSMSurfacePolygonType")
    .value("CrossWalk", ts::SurfacePolygonType::CrossWalk)
    .value("Junction", ts::SurfacePolygonType::Junction)
    .value("SideWalk", ts::SurfacePolygonType::SideWalk)
    .value("SpeedBump", ts::SurfacePolygonType::SpeedBump)
    .value("Surface", ts::SurfacePolygonType::Surface)
    .value("TrainTracks", ts::SurfacePolygonType::TrainTracks)
    .value("Unknown", ts::SurfacePolygonType::Unknown)
  ;

  // ===========================================================================
  // -- OSM Map Data Converter ------------------------------------------------
  // ===========================================================================

  class_<crod::OSMMapDataConverter>("OSMMapDataConverter", no_init)
    .def("convert_osm_way_type_to_lane_type", &crod::OSMMapDataConverter::ConvertOSMWayTypeToLaneType, (args("osm_way_type")))
    .staticmethod("convert_osm_way_type_to_lane_type")
    .def("convert_ts_lane_type_to_carla_lane_type", &crod::OSMMapDataConverter::ConvertTSLaneTypeToCarlaLaneType, (args("ts_type")))
    .staticmethod("convert_ts_lane_type_to_carla_lane_type")
    .def("convert_ts_road_type_to_carla_road_type", &crod::OSMMapDataConverter::ConvertTSRoadTypeToCarlaRoadType, (args("ts_type")))
    .staticmethod("convert_ts_road_type_to_carla_road_type")
    .def("convert_ts_boundary_type_to_lane_marking", &crod::OSMMapDataConverter::ConvertTSBoundaryTypeToLaneMarking, (args("ts_boundary")))
    .staticmethod("convert_ts_boundary_type_to_lane_marking")
    .def("convert_ts_boundary_color_to_lane_marking_color", &crod::OSMMapDataConverter::ConvertTSBoundaryColorToLaneMarkingColor, (args("ts_color")))
    .staticmethod("convert_ts_boundary_color_to_lane_marking_color")
    .def("convert_lane_direction_to_navigable", &crod::OSMMapDataConverter::ConvertLaneDirectionToNavigable, (args("direction")))
    .staticmethod("convert_lane_direction_to_navigable")
    .def("convert_surface_polygon_type_to_lane_type", &crod::OSMMapDataConverter::ConvertSurfacePolygonTypeToLaneType, (args("surface_type")))
    .staticmethod("convert_surface_polygon_type_to_lane_type")
  ;
}