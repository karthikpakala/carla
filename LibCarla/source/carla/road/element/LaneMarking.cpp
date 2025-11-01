// Copyright (c) 2025 Computer Vision Center (CVC) at the Universitat Autonoma
// de Barcelona (UAB).
//
// This work is licensed under the terms of the MIT license.
// For a copy, see <https://opensource.org/licenses/MIT>.

#include "carla/road/element/LaneMarking.h"

#include "carla/Exception.h"
#include "carla/StringUtil.h"
#include "carla/road/element/RoadInfoMarkRecord.h"

namespace carla {
namespace road {
namespace element {

  static LaneMarking::Type GetType(std::string str) {
    StringUtil::ToLower(str);
    if (str == "solid") {
      return LaneMarking::Type::Solid;
    } else if (str == "double solid" || str == "solid solid") {
      return LaneMarking::Type::DoubleSolid;
    } else if (str == "dashed solid") {
      return LaneMarking::Type::DashedSolid;
    } else if (str == "solid dashed") {
      return LaneMarking::Type::SolidDashed;
    } else if (str == "dashed" || str == "broken") {
      return LaneMarking::Type::Dashed;
    } else if (str == "double dashed") {
      return LaneMarking::Type::DoubleDashed;
    } else if (str == "reflectors only") {
      return LaneMarking::Type::ReflectorsOnly;
    } else if (str == "curb") {
      return LaneMarking::Type::Curb;
    } else if (str == "none") {
      return LaneMarking::Type::None;
    } else {
      return LaneMarking::Type::NotSet;
    }
  }

  static LaneMarking::Color GetColor(std::string str) {
    StringUtil::ToLower(str);
    if (str == "white" || str == "standard") {
      return LaneMarking::Color::White;
    } else if (str == "yellow") {
      return LaneMarking::Color::Yellow;
    } else if (str == "orange") {
      return LaneMarking::Color::Orange;
    } else {
      return LaneMarking::Color::NotSet;
    }
  }

  static LaneMarking::LaneChange GetLaneChange(RoadInfoMarkRecord::LaneChange lane_change, bool isRHT) {
    switch (lane_change) {
      case RoadInfoMarkRecord::LaneChange::Increase:
        return isRHT ? LaneMarking::LaneChange::Right : LaneMarking::LaneChange::Left;
      case RoadInfoMarkRecord::LaneChange::Decrease:
        return isRHT ? LaneMarking::LaneChange::Left : LaneMarking::LaneChange::Right;
      case RoadInfoMarkRecord::LaneChange::Both:
        return LaneMarking::LaneChange::Both;
      default:
        return LaneMarking::LaneChange::None;
    }
  }

  LaneMarking::LaneMarking(const RoadInfoMarkRecord &info)
    : type(GetType(info.GetType())),
      color(GetColor(info.GetColor())),
      lane_change(GetLaneChange(info.GetLaneChange(), info.isRHT())),
      width(info.GetWidth()) {}

} // namespace element
} // namespace road
} // namespace carla
