
import pygame
import numpy

from typing import Tuple
from scipy import stats

from lidar_display import scan_contour

WHITE = (255, 255, 255)
RED = (255,0,0)
PINK = (255,0,255)
GREEN = (0,255,0)
BLUE = (0,0,255)
GREY = (100, 100, 100)

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

    draw_sc(screen, sc, BLUE)

    smoothing_scale = 1.0

    smoothed_sc = smooth(sc, smoothing_scale)
    draw_sc(screen, smoothed_sc, RED)

    damping_values = []
    for i in range(len(sc.points)):
        p1 = sc.points[i]
        p2 = smoothed_sc.points[i]
        pygame.draw.aaline(
            screen,
            GREY,
            _space_to_pixels(p1.x, p1.y),
            _space_to_pixels(p2.x, p2.y))

        d = scan_contour.distance(p1, p2)
        damping_value = 2 * d / smoothing_scale * numpy.exp(-2 * d / smoothing_scale)
        damping_values.append(damping_value)

    for i in range(1, len(damping_values)-1):
        cur = damping_values[i]
        if cur > 0.3 and cur > damping_values[i-1] and cur > damping_values[i+1]:
            p1 = sc.points[i]
            pygame.draw.circle(screen, PINK, _space_to_pixels(p1.x, p1.y), 5)


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

