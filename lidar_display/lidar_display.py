import pygame
import time
import sys
import os.path
import math

sys.path.append(os.path.join(os.path.dirname(__file__), '../out'))

import lidarpy

WHITE = (255, 255, 255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
GREY = (100, 100, 100)

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    lidar = lidarpy.Lidar("/dev/tty.usbserial-0001")
    if not lidar.connect():
        print('failed to connect')
        sys.exit(1)

    lidar.start_motor()
    sh = lidarpy.ScanHolder()

    center = (400, 300)
    pixels_per_meter = 300.0 / 5
    unknown_length = 400

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return

        screen.fill(WHITE)

        if not lidar.get_scan(sh):
            print('failed to get scan')
            time.sleep(0.1)
            continue

        print(f'dist: {sh.distance_meters(0)}')

        pygame.draw.circle(screen, RED, center, pixels_per_meter, 1)
        pygame.draw.circle(screen, RED, center, pixels_per_meter * 2, 1)
        pygame.draw.circle(screen, RED, center, pixels_per_meter * 3, 1)
        pygame.draw.circle(screen, RED, center, pixels_per_meter * 4, 1)
        pygame.draw.circle(screen, RED, center, pixels_per_meter * 5, 1)

        max_dist = 0.0
        for i in range(0, sh.num_points()):
            angle_rad = sh.angle_deg(i) * math.pi / 180.0
            distance_meters = sh.distance_meters(i)
            if distance_meters > max_dist:
                max_dist = distance_meters
            if distance_meters == 0.0:
                distance_pixels = unknown_length
                color = GREY
            else:
                distance_pixels = distance_meters * pixels_per_meter
                color = BLUE

            offset_x = distance_pixels * math.sin(angle_rad)
            offset_y = distance_pixels * -math.cos(angle_rad)
            end_point = (center[0] + offset_x, center[1] + offset_y)
            pygame.draw.aaline(screen, color, center, end_point)
        print(f'max dist: {max_dist}')
        pygame.display.update()

    lidar.stop_motor()


if __name__ == '__main__':
    main()
