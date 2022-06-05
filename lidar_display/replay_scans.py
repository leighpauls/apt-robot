import os.path
import pickle
import time
import pygame

from lidar_display import scan_contour, draw_frame

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    scan_dir = os.path.join(os.path.dirname(__file__), 'scans')

    while True:
        for i in range(20):

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return

            print(f'replay {i}')

            with open(os.path.join(scan_dir, f'scan_{i}.pickle'), 'rb') as f:
                sc = pickle.load(f)

            draw_frame.draw_frame(screen, sc)
            pygame.display.update()
            time.sleep(1.0)

if __name__ == '__main__':
    main()