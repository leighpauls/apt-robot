import pygame
import time
import math
from typing import List, NamedTuple, Tuple

from lidar_display import lidar_reader, lidarpy, draw_frame


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
            time.sleep(1.0)
            continue

        draw_frame.draw_frame(screen, sc)

        pygame.display.update()

    lidar.stop_motor()



if __name__ == '__main__':
    main()
