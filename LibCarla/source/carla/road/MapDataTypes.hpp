// CONFIDENTIAL - do not disclose, distribute, or alter without express permission by TORC Robotics.
// All use subject to express agreement only. No implied use or license.
//
// Software copyrights by TORC Robotics, Inc as of initial publish date.
//
// Unless required by applicable law or agreed in writing, use of software is on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

#pragma once

#include <cstdint>

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
    // Legacy compatibility values from old CARLA enum
    None          = 6,
    Driving       = 1,  // Alias for Standard
    Parking       = 7,
    Bidirectional = 8,
    Shoulder      = 9,
    Sidewalk      = 10,
    Biking        = 11,
    Any           = 255 // Special value for "any lane type"
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
