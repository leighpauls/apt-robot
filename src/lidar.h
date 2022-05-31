#pragma once

#include "rplidar.h"

#include <memory>
#include <string>
#include <vector>

namespace lidar {

struct ScanPoint {
public:
  ScanPoint() = default;
  ScanPoint(float angle_deg, float distance_meters);

  float angle_deg;
  float distance_meters;
};

class ScanHolder {
public:
  ScanHolder() = default;
  size_t numPoints();
  float angleDeg(size_t point_num);
  float distanceMeters(size_t point_num);

  void assignPoints(rplidar_response_measurement_node_t *nodes, size_t count);

private:
  std::vector<ScanPoint> _scan_points;
};

class Lidar {
public:
  Lidar(std::string dev_path);
  virtual ~Lidar();

  bool connect();
  bool startMotor();
  bool stopMotor();
  bool getScan(std::shared_ptr<ScanHolder> dest);

private:
  std::string _dev_path;
  rp::standalone::rplidar::RPlidarDriver* _driver;
};
} // namespace lidar
