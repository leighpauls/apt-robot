import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '../out'))

import pygame
import time
import math
from typing import List, NamedTuple, Tuple

import lidarpy

from lidar_display import lidar_reader

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

    reader = lidar_reader.LidarReader(lidar)


    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return

        try:
            sc = reader.fetch_contour_from_lidar()
        except lidar_reader.FetchLidarError as e:
            print(f'Fetch error: {e}')
            time.sleep(0.1)
            continue

        screen.fill(WHITE)

        pygame.draw.circle(screen, RED, center, pixels_per_meter, 1)
        pygame.draw.circle(screen, RED, center, pixels_per_meter * 2, 1)
        pygame.draw.circle(screen, RED, center, pixels_per_meter * 3, 1)
        pygame.draw.circle(screen, RED, center, pixels_per_meter * 4, 1)
        pygame.draw.circle(screen, RED, center, pixels_per_meter * 5, 1)


        for p in sc.points:
            pygame.draw.circle(screen, GREEN, _space_to_pixels(p.x, p.y), 3)

        contour_length = sc.loop_length()
        step_length_meters = 0.05
        prev_dist = 0.0
        while prev_dist < contour_length:
            next_dist = prev_dist + step_length_meters

            next_cp = sc.find_point_on_curve(next_dist)
            prev_cp = sc.find_point_on_curve(prev_dist)

            pygame.draw.aaline(
                screen,
                BLUE,
                _space_to_pixels(prev_cp.x, prev_cp.y), _space_to_pixels(next_cp.x, next_cp.y))

            prev_dist = next_dist

        pygame.display.update()

    lidar.stop_motor()

def _space_to_pixels(x_meters: float, y_meters: float) -> Tuple[float, float]:
    offset_x_pixels = pixels_per_meter * -1 * y_meters
    offset_y_pixels = pixels_per_meter * -1 * x_meters
    return (center[0] + offset_x_pixels, center[1] + offset_y_pixels)


if __name__ == '__main__':
    main()
