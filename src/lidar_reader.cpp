
#include "lidar.h"

#include <iostream>
#include <thread>

namespace {

using lidar::Lidar;
using lidar::ScanHolder;

bool exiting = false;

void sigint_callback_handler(int signum) {
  std::cout << "Caught sigint" << std::endl;
  exiting = true;
}

int do_main() {
  Lidar lidar("/dev/tty.usbserial-0001");
  if (!lidar.connect()) {
    std::cout << "Error connecting." << std::endl;
    return 1;
  }

  lidar.startMotor();

  signal(SIGINT, sigint_callback_handler);

  auto scan_holder = std::make_shared<ScanHolder>();
  while (!exiting) {
    if (!lidar.getScan(scan_holder)) {
      std::cout << "Failed to get scan" << std::endl;
    } else {
      std::cout << "Frames " << scan_holder->numPoints()
                << " Angle: " << scan_holder->angleDeg(0)
                << " Dist: " << scan_holder->distanceMeters(0) << std::endl;
    }
  }

  std::cout << "Stopping motor" << std::endl;
  lidar.stopMotor();

  std::cout << "exiting motor" << std::endl;

  return 0;
}

} // namespace

int main(int argc, char **argv) { return do_main(); }
