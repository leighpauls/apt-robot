
import pygame
import numpy

from typing import Tuple, List
from scipy import stats

from lidar_display import scan_contour

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
    screen.fill(WHITE)

    pygame.draw.circle(screen, RED, center, pixels_per_meter, 1)
    pygame.draw.circle(screen, RED, center, pixels_per_meter * 2, 1)
    pygame.draw.circle(screen, RED, center, pixels_per_meter * 3, 1)
    pygame.draw.circle(screen, RED, center, pixels_per_meter * 4, 1)
    pygame.draw.circle(screen, RED, center, pixels_per_meter * 5, 1)

    # draw the raw contour
    draw_sc(screen, sc, BLUE)

    sorted_landmarks = get_landmarks(sc)
    for l, w in sorted_landmarks[:20]:
        pygame.draw.circle(screen, BLACK, _space_to_pixels(l.x, l.y), 5)


def get_landmarks(sc: scan_contour.ScanContourLoop) -> List[Tuple[scan_contour.ContourPoint, float]]:
    smoothing_scales = [(0.25, C1), (0.5, C2), (1.0, C3), (2.0, C4), (4.0, C5)]
    landmarks = []
    for s, c in smoothing_scales:
        landmarks += find_landmarks_for_smoothing_level(sc, s, c)
    sorted_landmarks = sorted(landmarks, key=lambda l: l[1], reverse=True)
    return sorted_landmarks


def find_landmarks_for_smoothing_level(
        sc: scan_contour.ScanContourLoop,
        smoothing_scale: float,
        color: Tuple) -> List[Tuple[scan_contour.ContourPoint, float]]:
    smoothed_sc = smooth(sc, smoothing_scale)

    damping_values = []
    for i in range(len(sc.points)):
        p1 = sc.points[i]
        p2 = smoothed_sc.points[i]

        d = scan_contour.distance(p1, p2)
        damping_value = 2 * d / smoothing_scale * numpy.exp(-2 * d / smoothing_scale)
        damping_values.append(damping_value)

    landmarks = []
    for i in range(1, len(damping_values)-2):
        cur = damping_values[i]
        if cur > max(
                0.2,
                damping_values[i-2],
                damping_values[i-1],
                damping_values[i+1],
                damping_values[i+2]):
            p1 = sc.points[i]
            landmarks.append((p1, cur))
    return landmarks


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


def smooth(sc: scan_contour.ScanContourLoop, scale: float) -> scan_contour.ScanContourLoop:
    smoothed_sc = scan_contour.ScanContourLoop()
    n = stats.norm()
    step_size = 6.0/100
    for p in sc.points:
        center_dist = p.distance
        x = 0.0
        y = 0.0
        for dist_offset in numpy.arange(-3.0, 3.0, step_size):
            sample_point = sc.find_point_on_curve(p.distance + dist_offset * scale)
            weight = n.pdf(dist_offset) * step_size
            x += sample_point.x * weight
            y += sample_point.y * weight
        smoothed_sc.add_point(x, y)
    return smoothed_sc

def _space_to_pixels(x_meters: float, y_meters: float) -> Tuple[float, float]:
    offset_x_pixels = pixels_per_meter * -1 * y_meters
    offset_y_pixels = pixels_per_meter * -1 * x_meters
    return (center[0] + offset_x_pixels, center[1] + offset_y_pixels)

