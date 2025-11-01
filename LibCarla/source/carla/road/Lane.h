// Copyright (c) 2025 Computer Vision Center (CVC) at the Universitat Autonoma
// de Barcelona (UAB).
//
// This work is licensed under the terms of the MIT license.
// For a copy, see <https://opensource.org/licenses/MIT>.

#pragma once

#include "carla/geom/Mesh.h"
#include "carla/geom/Transform.h"
#include "carla/road/InformationSet.h"
#include "carla/road/RoadTypes.h"
#include "carla/road/MapDataTypes.h"

#include <vector>
#include <iostream>
#include <memory>

namespace carla {
namespace road {

  class LaneSection;
  class MapBuilder;
  class Road;

  class Lane : private MovableNonCopyable {
  public:

    // Use the new LaneType from MapDataTypes.hpp
    using LaneType = ts::LaneType;

  public:

    Lane() = default;

    Lane(
        LaneSection *lane_section,
        LaneId id,
        std::vector<std::unique_ptr<element::RoadInfo>> &&info)
      : _lane_section(lane_section),
        _id(id),
        _info(std::move(info)) {
      DEBUG_ASSERT(lane_section != nullptr);
    }

    const LaneSection *GetLaneSection() const;

    Road *GetRoad() const;

    LaneId GetId() const;

    ts::LaneType GetType() const;

    bool GetLevel() const;

    template <typename T>
    const T *GetInfo(const double s) const {
      DEBUG_ASSERT(_lane_section != nullptr);
      return _info.GetInfo<T>(s);
    }

    template <typename T>
    std::vector<const T*> GetInfos() const {
      DEBUG_ASSERT(_lane_section != nullptr);
      return _info.GetInfos<T>();
    }

    const std::vector<Lane *> &GetNextLanes() const {
      return _next_lanes;
    }

    const std::vector<Lane *> &GetPreviousLanes() const {
      return _prev_lanes;
    }

    LaneId GetSuccessor() const {
      return _successor;
    }

    LaneId GetPredecessor() const {
      return _predecessor;
    }

    double GetDistance() const;

    double GetLength() const;

    /// Returns the total lane width given a s
    double GetWidth(const double s) const;

    /// Checks whether the geometry is straight or not
    bool IsStraight() const;

    geom::Transform ComputeTransform(const double s) const;

    /// Computes the location of the edges given a s
    std::pair<geom::Vector3D, geom::Vector3D> GetCornerPositions(
      const double s, const float extra_width = 0.f) const;

    bool IsPositiveDirection() const;

  private:

    friend MapBuilder;

    LaneSection *_lane_section = nullptr;

    LaneId _id = 0;

    InformationSet _info;

    ts::LaneType _type = ts::LaneType::NotSet;

    bool _level = false;

    LaneId _successor = 0;

    LaneId _predecessor = 0;

    std::vector<Lane *> _next_lanes;

    std::vector<Lane *> _prev_lanes;
  };

} // road
} // carla
