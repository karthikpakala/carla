// Copyright (c) 2025 Computer Vision Center (CVC) at the Universitat Autonoma
// de Barcelona (UAB).
//
// This work is licensed under the terms of the MIT license.
// For a copy, see <https://opensource.org/licenses/MIT>.

#pragma once

#include <cstdint>
#include <string>

namespace carla {
namespace road {

  using RoadId = uint32_t;

  using JuncId = int32_t;

  using LaneId = int32_t;

  using SectionId = uint32_t;

  using ObjId = uint32_t;

  using SignId = std::string;

  using StencilId = std::string;

  using ConId = uint32_t;

  using ContId = std::string;

} // road
} // carla

// Custom OSM map data types for enhanced map support
namespace ts
{

enum class RoadType : std::uint8_t
{
    NotSet           = 0,
    Highway          = 1,
    SurfaceStreet    = 2,
    Intersection     = 3,
    HighwayConnector = 4,
};

enum class LaneBoundaryType : std::uint8_t
{
    NotSet         = 0,
    None           = 1,
    Solid          = 2,
    DoubleSolid    = 3,
    DashedSolid    = 4, // dashed on left, solid on right (relative to polyline direction)
    SolidDashed    = 5, // solid on left, dashed on right (relative to polyline direction)
    Dashed         = 6,
    DoubleDashed   = 7,
    ReflectorsOnly = 8,
    Curb           = 9,
};

enum class LaneType : std::uint8_t
{
    NotSet     = 0,
    Standard   = 1,
    HovLane    = 2,
    BikeLane   = 3,
    NoTrucks   = 4,
    Restricted = 5,
};

enum class LaneRightOfWay : std::uint8_t
{
    Continue      = 0,
    Stop          = 1,
    Yield         = 2,
    TrafficSignal = 3,
};

enum class LaneBoundaryColor : std::uint8_t
{
    NotSet = 0,
    White  = 1,
    Yellow = 2,
    Orange = 3,
};

enum class LaneBlockageState : std::uint8_t
{
    NotBlocked = 0,
    Blocked    = 1,
};

enum class LaneDirection : std::int8_t
{
    Backward = -1,
    Both     = 0,
    Forward  = 1,
};

enum class SurfacePolygonType : std::uint8_t
{
    CrossWalk   = 0,  // drivable area in which pedestrians should be expected
    Junction    = 1,  // area where roads meet and lanes join
    SideWalk    = 2,  // non-drivable area in which pedestrians should be expected
    SpeedBump   = 3,  // hump or other surface disturbance meant for traffic-calming
    Surface     = 4,  // drivable surface, which is traversable pavement not designated exclusively for pedestrians
    TrainTracks = 5,  // you know what train tracks are
    Unknown     = 99, // Unknown type
};

} // namespace ts

namespace carla {
namespace road {
  // Import custom types from ts namespace for OSM support
  using TSRoadType = ts::RoadType;
  using TSLaneBoundaryType = ts::LaneBoundaryType;
  using TSLaneType = ts::LaneType;
  using TSLaneRightOfWay = ts::LaneRightOfWay;
  using TSLaneBoundaryColor = ts::LaneBoundaryColor;
  using TSLaneBlockageState = ts::LaneBlockageState;
  using TSLaneDirection = ts::LaneDirection;
  using TSSurfacePolygonType = ts::SurfacePolygonType;
} // road
} // carla
