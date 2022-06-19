from typing import Tuple, List
from lidar_display import scan_contour
from scipy import stats
import numpy

def get_landmarks(sc: scan_contour.ScanContourLoop) -> List[Tuple[scan_contour.ContourPoint, float]]:
    smoothing_scales = [0.25, 0.5, 1.0, 2.0, 4.0]
    landmarks = []
    for s in smoothing_scales:
        landmarks += find_landmarks_for_smoothing_level(sc, s)
    sorted_landmarks = sorted(landmarks, key=lambda l: l[1], reverse=True)
    return sorted_landmarks


def find_landmarks_for_smoothing_level(
        sc: scan_contour.ScanContourLoop,
        smoothing_scale: float) -> List[Tuple[scan_contour.ContourPoint, float]]:
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
