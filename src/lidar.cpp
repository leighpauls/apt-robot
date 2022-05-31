#include "lidar.h"

namespace lidar {

using rp::standalone::rplidar::DRIVER_TYPE_SERIALPORT;
using rp::standalone::rplidar::RPlidarDriver;

const size_t MEASUREMENT_NODES = 8192;

ScanPoint::ScanPoint(float angle_deg, float distance_meters)
    : angle_deg(angle_deg), distance_meters(distance_meters) {}

size_t ScanHolder::numPoints() { return _scan_points.size(); }

float ScanHolder::angleDeg(size_t point_num) {
  return _scan_points[point_num].angle_deg;
}

float ScanHolder::distanceMeters(size_t point_num) {
  return _scan_points[point_num].distance_meters;
}

void ScanHolder::assignPoints(rplidar_response_measurement_node_t *nodes,
                              size_t count) {
  _scan_points.resize(count);
  for (size_t i = 0; i < count; i++) {
    auto node = nodes[i];
    float angle =
        (node.angle_q6_checkbit >> RPLIDAR_RESP_MEASUREMENT_ANGLE_SHIFT) / 64.f;
    auto dist = node.distance_q2 / 4.0f;

    _scan_points[i] = ScanPoint(angle, dist);
  }
}

Lidar::Lidar(std::string dev_path) : _dev_path(dev_path), _driver(nullptr) {}

Lidar::~Lidar() {
  if (_driver) {
    _driver->stopMotor();
    RPlidarDriver::DisposeDriver(_driver);
  }
}

bool Lidar::connect() {
  if (_driver) {
    return false;
  }

  auto new_driver = RPlidarDriver::CreateDriver(DRIVER_TYPE_SERIALPORT);
  if (!new_driver) {
    return false;
  }

  if (IS_FAIL(new_driver->connect(_dev_path.c_str(), 115200))) {
    return false;
  }

  _driver = new_driver;
  return true;
}

bool Lidar::startMotor() {
  if (!_driver) {
    return false;
  }
  _driver->startMotor();
  return true;
}

bool Lidar::stopMotor() {
  if (!_driver) {
    return false;
  }
  _driver->stopMotor();
  return true;
}

bool Lidar::getScan(std::shared_ptr<ScanHolder> dest) {
  if (!_driver || !dest) {
    return false;
  }

  if (IS_FAIL(_driver->startScan(0, 1))) {
    return false;
  }

  // TODO: make nodes object-level
  rplidar_response_measurement_node_t nodes[MEASUREMENT_NODES];
  size_t count = MEASUREMENT_NODES;
  u_result ans = _driver->grabScanData(nodes, count);

  if (!IS_OK(ans) && ans != RESULT_OPERATION_TIMEOUT) {
    return false;
  }

  _driver->ascendScanData(nodes, count);

  dest->assignPoints(nodes, count);
  return true;
}
} // namespace lidar
