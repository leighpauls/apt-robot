
import pygame
import numpy

from typing import Tuple, List

from lidar_display import scan_contour, landmarks

WHITE = (255, 255, 255)
RED = (255,0,0)
PINK = (255,0,255)
GREEN = (0,255,0)
BLUE = (0,0,255)
GREY = (100, 100, 100)
BLACK = (0, 0, 0)

C1 = (0, 0, 0)
C2 = (25, 25, 25)
C3 = (50, 50, 50)
C4 = (75, 75, 75)
C5 = (100, 100, 100)


center = (400, 300)
pixels_per_meter = 300.0 / 5
unknown_length = 16 * pixels_per_meter


def draw_frame(screen, sc: scan_contour.ScanContourLoop) -> None:
    draw_background(screen)

    # draw the raw contour
    draw_sc(screen, sc, BLUE)

    sorted_landmarks = landmarks.get_landmarks(sc)
    for l, w in sorted_landmarks[:20]:
        pygame.draw.circle(screen, BLACK, _space_to_pixels(l.x, l.y), 5)

def draw_background(screen) -> None:
    screen.fill(WHITE)

    pygame.draw.circle(screen, RED, center, pixels_per_meter, 1)
    pygame.draw.circle(screen, RED, center, pixels_per_meter * 2, 1)
    pygame.draw.circle(screen, RED, center, pixels_per_meter * 3, 1)
    pygame.draw.circle(screen, RED, center, pixels_per_meter * 4, 1)
    pygame.draw.circle(screen, RED, center, pixels_per_meter * 5, 1)



def draw_sc(screen, sc: scan_contour.ScanContourLoop, color: Tuple[int, int, int]) -> None:
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
            color,
            _space_to_pixels(prev_cp.x, prev_cp.y), _space_to_pixels(next_cp.x, next_cp.y))

        prev_dist = next_dist


def _space_to_pixels(x_meters: float, y_meters: float) -> Tuple[float, float]:
    offset_x_pixels = pixels_per_meter * -1 * y_meters
    offset_y_pixels = pixels_per_meter * -1 * x_meters
    return (center[0] + offset_x_pixels, center[1] + offset_y_pixels)

