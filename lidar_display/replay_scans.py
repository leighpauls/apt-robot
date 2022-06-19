from typing import Tuple, List
import os.path
import pickle
import time
import pygame
import queue
import threading
import sys
import random

from lidar_display import scan_contour, draw_frame, landmarks

new_landmarks_queue = queue.SimpleQueue()

def process_scans() -> None:
    work_complete = False
    try:
        scan_dir = os.path.join(os.path.dirname(__file__), 'scans')

        for i in range(20):
            print(f'replay {i}')

            with open(os.path.join(scan_dir, f'scan_{i}.pickle'), 'rb') as f:
                sc = pickle.load(f)

            new_landmarks_queue.put(landmarks.get_landmarks(sc))
        work_complete = True
    finally:
        if not work_complete:
            sys.exit(1)

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    landmark_list = []

    t = threading.Thread(target=process_scans, daemon=True)
    t.start()

    draw_frame.draw_background(screen)
    pygame.display.update()

    colors = {}

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                print('Exiting...')
                sys.exit(0)
        time.sleep(1.0)

        try:
            new_landmarks = new_landmarks_queue.get(block=False)
            print('got new landmarks!')
            landmark_list.append(new_landmarks)
            sig = create_signature([l for l, w in new_landmarks])
            print(sig)
        except queue.Empty:
            continue

        draw_frame.draw_background(screen)

        for j in range(len(landmark_list)):
            if not j in colors:
                colors[j] = (
                    int(random.randrange(0, 255, 1)),
                    int(random.randrange(0, 255, 1)),
                    int(random.randrange(0, 255, 1)))
            c = colors[j]
            for l, w in landmark_list[j]:
                pygame.draw.circle(screen, c, draw_frame._space_to_pixels(l.x, l.y), 5)

        pygame.display.update()


MAX_DIST_BUCKET = 10.0
NUM_BUCKETS = 10

def create_signature(points: List[scan_contour.ContourPoint]) -> List[float]:
    histogram = [0.0] * NUM_BUCKETS

    # Normalization factor
    n = 1.0 / len(points)
    kernel = {-1: 0.25*n, 0: 0.5*n, 1: 0.25*n}

    for i in range(0, len(points)):
        for j in range(i+1, len(points)):
            dist = scan_contour.distance(points[i], points[j])
            center_bucket = int(NUM_BUCKETS * dist / MAX_DIST_BUCKET)
            center_bucket = max(0, min(NUM_BUCKETS - 1, center_bucket))
            for diff, p in kernel.items():
                bucket = center_bucket + diff
                if bucket >= 0 and bucket < NUM_BUCKETS:
                    histogram[bucket] += p
    return histogram

if __name__ == '__main__':
    main()
