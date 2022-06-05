
from lidar_display import scan_contour

import lidarpy
import math

class FetchLidarError(Exception):
    ...

class LidarReader:
    def __init__(self, lidar: lidarpy.Lidar) -> None:
        self.lidar = lidar
        self.sh = lidarpy.ScanHolder()

    def fetch_contour_from_lidar(self) -> scan_contour.ScanContourLoop:
        if not self.lidar.get_scan(self.sh):
            raise FetchLidarError('failed to get scan')

        sc = scan_contour.ScanContourLoop()
        for i in range(0, self.sh.num_points()):
            angle_rad = -self.sh.angle_deg(i) * math.pi / 180.0
            distance_meters = self.sh.distance_meters(i)

            if distance_meters == 0.0:
                continue

            offset_x_meters = distance_meters * math.cos(angle_rad)
            offset_y_meters = distance_meters * math.sin(angle_rad)
            sc.add_point(offset_x_meters, offset_y_meters)

        return sc

