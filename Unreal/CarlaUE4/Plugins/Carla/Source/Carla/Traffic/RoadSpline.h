#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Components/SplineComponent.h"
#include "RoadSpline.generated.h"

UENUM(BlueprintType)
enum class ERoadSplineBoundaryType : uint8
{
  None          UMETA(DisplayName = "None"),
  Driving       UMETA(DisplayName = "Driving"),
  Stop          UMETA(DisplayName = "Stop"),
  Shoulder      UMETA(DisplayName = "Shoulder"),
  Biking        UMETA(DisplayName = "Biking"),
  Sidewalk      UMETA(DisplayName = "Sidewalk"),
  Border        UMETA(DisplayName = "Border"),
  Restricted    UMETA(DisplayName = "Restricted"),
  Parking       UMETA(DisplayName = "Parking"),
  Bidirectional UMETA(DisplayName = "Bidirectional"),
  Median        UMETA(DisplayName = "Median"),
  Special1      UMETA(DisplayName = "Special1"),
  Special2      UMETA(DisplayName = "Special2"),
  Special3      UMETA(DisplayName = "Special3"),
  RoadWorks     UMETA(DisplayName = "RoadWorks"),
  Tram          UMETA(DisplayName = "Tram"),
  Rail          UMETA(DisplayName = "Rail"),
  Entry         UMETA(DisplayName = "Entry"),
  Exit          UMETA(DisplayName = "Exit"),
  OffRamp       UMETA(DisplayName = "OffRamp"),
  OnRamp        UMETA(DisplayName = "OnRamp"),
  Unknown       UMETA(DisplayName = "Unknown"),
  // OSM-compatible boundary types
  Solid         UMETA(DisplayName = "Solid"),
  DoubleSolid   UMETA(DisplayName = "DoubleSolid"),
  DashedSolid   UMETA(DisplayName = "DashedSolid"),
  SolidDashed   UMETA(DisplayName = "SolidDashed"),
  Dashed        UMETA(DisplayName = "Dashed"),
  DoubleDashed  UMETA(DisplayName = "DoubleDashed"),
  ReflectorsOnly UMETA(DisplayName = "ReflectorsOnly"),
  Curb          UMETA(DisplayName = "Curb"),
  Standard      UMETA(DisplayName = "Standard"),
  HovLane       UMETA(DisplayName = "HovLane"),
  BikeLane      UMETA(DisplayName = "BikeLane"),
  NoTrucks      UMETA(DisplayName = "NoTrucks")
};

UENUM(BlueprintType)
enum class ERoadSplineOrientationType : uint8
{
  Unkown        UMETA(DisplayName = "Unkown"),
  Left          UMETA(DisplayName = "Left"),
  Right         UMETA(DisplayName = "Right"),
  Center        UMETA(DisplayName = "Center"),
};

UCLASS()
class CARLA_API ARoadSpline : public AActor
{
  GENERATED_BODY()

public:
  ARoadSpline();

  UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Spline")
  USplineComponent* SplineComponent;

  UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Boundary")
  ERoadSplineBoundaryType BoundaryType;

  UPROPERTY(VisibleAnywhere, BlueprintReadWrite, Category = "Boundary")
  ERoadSplineOrientationType OrientationType;

  UPROPERTY(VisibleAnywhere, BlueprintReadWrite, Category = "RoadInfo")
  bool bIsJunction;

  UPROPERTY(VisibleAnywhere, BlueprintReadWrite, Category = "RoadInfo")
  int RoadID;

  UPROPERTY(VisibleAnywhere, BlueprintReadWrite, Category = "RoadInfo")
  int LaneID;

  // OSM-specific properties
  UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "OSM")
  uint8 OSMRoadType = 0;  // ts::RoadType

  UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "OSM") 
  uint8 OSMLaneType = 0;  // ts::LaneType

  UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "OSM")
  uint8 OSMBoundaryColor = 0;  // ts::LaneBoundaryColor

  UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "OSM")
  uint8 OSMRightOfWay = 0;  // ts::LaneRightOfWay

  UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "OSM")
  int8 OSMLaneDirection = 1;  // ts::LaneDirection

  void SetSplinePoints(const TArray<FVector>& Points, bool bClosedLoop = false);
};

