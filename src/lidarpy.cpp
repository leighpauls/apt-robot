#include <memory>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <string>

#include "lidar.h"

namespace py = pybind11;

using lidar::Lidar;
using lidar::ScanHolder;

PYBIND11_MODULE(lidarpy, m) {
  m.doc() = "Pythong bindings for lidar";

  py::class_<ScanHolder, std::shared_ptr<ScanHolder>>(m, "ScanHolder")
      .def(py::init<>())
      .def("num_points", &ScanHolder::numPoints)
      .def("angle_deg", &ScanHolder::angleDeg)
      .def("distance_meters", &ScanHolder::distanceMeters);

  py::class_<Lidar>(m, "Lidar")
      .def(py::init<std::string>())
      .def("connect", &Lidar::connect)
      .def("start_motor", &Lidar::startMotor)
      .def("stop_motor", &Lidar::stopMotor)
      .def("get_scan", &Lidar::getScan);
}
