import pygame
import time
import sys
import os.path
import math
from typing import List, NamedTuple, Tuple

sys.path.append(os.path.join(os.path.dirname(__file__), '../out'))

import lidarpy

class ContourPoint(NamedTuple):
    x: float
    y: float
    distance: float

class ScanContourLoop:
    points: List[ContourPoint]

    def __init__(self):
        self.points = []

    def add_point(self, x: float, y: float):
        if len(self.points) == 0:
            new_distance = 0
        else:
            prev_point = self.points[-1]
            dx = x - prev_point.x
            dx = y - prev_point.y
            new_distance = prev_point.distance + _distance(x, y, prev_point.x, prev_point.y)

        self.points.append(ContourPoint(x, y, new_distance))

    def loop_length(self) -> float:
        if len(self.points) < 2:
            return 0
        first = self.points[0]
        last = self.points[-1]
        return last.distance + _distance(first.x, first.y, last.x, last.y)

    def find_point_on_curve(self, distance: float) -> ContourPoint:
        if len(self.points) < 2:
            raise ValueError('Can not find point on empty curve')
        total_length = self.loop_length()
        distance = distance % total_length

        if distance > self.points[-1].distance:
            cur_point = self.points[-1]
            next_point = self.points[0]
        else:
            for i in range(1, len(self.points)):
                next_point = self.points[i]
                if distance <= next_point.distance:
                    cur_point = self.points[i-1]
                    break

        segment_length = next_point.distance - cur_point.distance
        dist_past_cur = distance - cur_point.distance
        bias = dist_past_cur / segment_length

        dx = next_point.x - cur_point.x
        dy = next_point.y - cur_point.y

        return ContourPoint(cur_point.x + dx * bias, cur_point.y + dy * bias, distance)

def _distance(x1, y1, x2, y2) -> float:
    dx = x1 - x2
    dy = y1 - y2
    return math.sqrt(dx*dx + dy*dy)

WHITE = (255, 255, 255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
GREY = (100, 100, 100)

center = (400, 300)
pixels_per_meter = 300.0 / 5
unknown_length = 16 * pixels_per_meter


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    lidar = lidarpy.Lidar("/dev/tty.usbserial-0001")
    if not lidar.connect():
        print('failed to connect')
        sys.exit(1)

    lidar.start_motor()
    sh = lidarpy.ScanHolder()


    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return

        screen.fill(WHITE)

        start_time = time.time()
        if not lidar.get_scan(sh):
            print('failed to get scan')
            time.sleep(0.1)
            continue
        end_time = time.time()
        print(f'get_scan latency: {end_time - start_time}')

        print(f'dist: {sh.distance_meters(0)}')

        pygame.draw.circle(screen, RED, center, pixels_per_meter, 1)
        pygame.draw.circle(screen, RED, center, pixels_per_meter * 2, 1)
        pygame.draw.circle(screen, RED, center, pixels_per_meter * 3, 1)
        pygame.draw.circle(screen, RED, center, pixels_per_meter * 4, 1)
        pygame.draw.circle(screen, RED, center, pixels_per_meter * 5, 1)

        max_dist = 0.0

        scan_contour = ScanContourLoop()
        for i in range(0, sh.num_points()):
            angle_rad = -sh.angle_deg(i) * math.pi / 180.0
            distance_meters = sh.distance_meters(i)
            if distance_meters > max_dist:
                max_dist = distance_meters

            if distance_meters == 0.0:
                continue

            offset_x_meters = distance_meters * math.cos(angle_rad)
            offset_y_meters = distance_meters * math.sin(angle_rad)
            scan_contour.add_point(offset_x_meters, offset_y_meters)

            new_point = _space_to_pixels(offset_x_meters, offset_y_meters)

            pygame.draw.circle(screen, GREEN, new_point, 3)


        contour_length = scan_contour.loop_length()
        step_length_meters = 0.05
        prev_dist = 0.0
        while prev_dist < contour_length:
            next_dist = prev_dist + step_length_meters

            next_cp = scan_contour.find_point_on_curve(next_dist)
            prev_cp = scan_contour.find_point_on_curve(prev_dist)

            pygame.draw.aaline(screen, BLUE, _space_to_pixels(prev_cp.x, prev_cp.y), _space_to_pixels(next_cp.x, next_cp.y))

            prev_dist = next_dist

        pygame.display.update()

    lidar.stop_motor()

def _space_to_pixels(x_meters: float, y_meters: float) -> Tuple[float, float]:
    offset_x_pixels = pixels_per_meter * -1 * y_meters
    offset_y_pixels = pixels_per_meter * -1 * x_meters
    return (center[0] + offset_x_pixels, center[1] + offset_y_pixels)


if __name__ == '__main__':
    main()
