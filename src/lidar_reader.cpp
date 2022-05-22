
#include "rplidar.h"

#include <iostream>
#include <thread>

namespace {

using rp::standalone::rplidar::DRIVER_TYPE_SERIALPORT;
using rp::standalone::rplidar::RPlidarDriver;

const size_t MEASUREMENT_NODES = 8192;

static bool exiting = false;

void sigint_callback_handler(int signum) {
  std::cout << "Caught sigint" << std::endl;
  exiting = true;
}

void doScan(RPlidarDriver *drv) {

  signal(SIGINT, sigint_callback_handler);

  for (int j = 0; j < 100; j++) {
    if (exiting) {
      std::cout << "exiting..." << std::endl;
      return;
    }
    if (IS_FAIL(drv->startScan(0, 1))) {
      std::cout << "failed to start scanning" << std::endl;
      return;
    }

    rplidar_response_measurement_node_t nodes[MEASUREMENT_NODES];
    size_t count = MEASUREMENT_NODES;
    u_result ans = drv->grabScanData(nodes, count);

    if (IS_OK(ans) || ans == RESULT_OPERATION_TIMEOUT) {
      drv->ascendScanData(nodes, count);

      std::cout << "Captured " << count << " nodes" << std::endl;

      size_t i = 0;
      auto node = nodes[i];
      float angle =
          (node.angle_q6_checkbit >> RPLIDAR_RESP_MEASUREMENT_ANGLE_SHIFT) /
          64.f;
      auto dist = node.distance_q2 / 4.0f;
      std::cout << "Frame " << i << ": " << angle << " deg " << dist << " mm"
                << std::endl;

    } else {
      std::cout << "Error grabbing scan data " << ans << std::endl;
    }
    // std::this_thread::sleep_for(1000ms);
  }
}

int do_main() {
  RPlidarDriver *drv = RPlidarDriver::CreateDriver(DRIVER_TYPE_SERIALPORT);

  if (!drv) {
    std::cout << "error creating driver" << std::endl;
    return 1;
  }

  if (IS_FAIL(drv->connect("/dev/tty.usbserial-0001", 115200))) {
    std::cout << "Error connecting" << std::endl;
    return 1;
  }

  drv->startMotor();

  doScan(drv);

  drv->stopMotor();

  RPlidarDriver::DisposeDriver(drv);
  return 0;
}

} // namespace

int main(int argc, char **argv) { return do_main(); }
