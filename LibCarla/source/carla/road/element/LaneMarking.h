// Copyright (c) 2025 Computer Vision Center (CVC) at the Universitat Autonoma
// de Barcelona (UAB).
//
// This work is licensed under the terms of the MIT license.
// For a copy, see <https://opensource.org/licenses/MIT>.

#pragma once

#include <cstdint>
#include <string>
#include "carla/road/MapDataTypes.h"

namespace carla {
namespace road {
namespace element {

  class RoadInfoMarkRecord;

  struct LaneMarking {

    // Use new boundary types from MapDataTypes.hpp
    using Type = ts::LaneBoundaryType;
    using Color = ts::LaneBoundaryColor;

    /// Can be used as flags.
    enum class LaneChange : uint8_t {
      None  = 0x00, // 00
      Right = 0x01, // 01
      Left  = 0x02, // 10
      Both  = 0x03  // 11
    };

    explicit LaneMarking(const RoadInfoMarkRecord &info);

    Type type = Type::NotSet;

    Color color = Color::NotSet;

    LaneChange lane_change = LaneChange::None;

    double width = 0.0;

    std::string GetColorInfoAsString(){
      switch(color){
        case Color::Yellow:
          return std::string("yellow");
          break;
        case Color::White:
          return std::string("white");
          break;
        case Color::Orange:
          return std::string("orange");
          break;
        default:
          return std::string("white");
          break;
      }
      return std::string("white");
    }
  };

} // namespace element
} // namespace road
} // namespace carla
