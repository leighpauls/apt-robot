from typing import Tuple
import os.path
import pickle
import time
import pygame

from lidar_display import scan_contour, draw_frame, landmarks

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    scan_dir = os.path.join(os.path.dirname(__file__), 'scans')

    landmark_list = []
    for i in range(20):

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return

        print(f'replay {i}')

        with open(os.path.join(scan_dir, f'scan_{i}.pickle'), 'rb') as f:
            sc = pickle.load(f)

        landmark_list.append(landmarks.get_landmarks(sc))

        draw_frame.draw_frame(screen, sc)

        for j in range(len(landmark_list)):
            c = j * 10
            for l, w in landmark_list[j]:
                pygame.draw.circle(screen, (c, c, c), draw_frame._space_to_pixels(l.x, l.y), 5)

        pygame.display.update()
        time.sleep(1.0)

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return


if __name__ == '__main__':
    main()
