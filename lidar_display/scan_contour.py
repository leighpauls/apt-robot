import math
from typing import List, NamedTuple, Tuple

class ContourPoint(NamedTuple):
    x: float
    y: float
    distance: float

def distance(p1: ContourPoint, p2: ContourPoint) -> float:
    return _distance(p1.x, p1.y, p2.x, p2.y)

class ScanContourLoop:
    points: List[ContourPoint]

    def __init__(self):
        self.points = []

    def add_point(self, x: float, y: float):
        if len(self.points) == 0:
            new_distance = 0
        else:
            prev_point = self.points[-1]
            dx = x - prev_point.x
            dx = y - prev_point.y
            new_distance = prev_point.distance + _distance(x, y, prev_point.x, prev_point.y)

        self.points.append(ContourPoint(x, y, new_distance))

    def loop_length(self) -> float:
        if len(self.points) < 2:
            return 0
        first = self.points[0]
        last = self.points[-1]
        return last.distance + distance(first, last)

    def find_point_on_curve(self, distance: float) -> ContourPoint:
        if len(self.points) < 2:
            raise ValueError('Can not find point on empty curve')
        total_length = self.loop_length()
        distance = distance % total_length

        if distance > self.points[-1].distance:
            cur_point = self.points[-1]
            next_point = self.points[0]
        else:
            for i in range(1, len(self.points)):
                next_point = self.points[i]
                if distance <= next_point.distance:
                    cur_point = self.points[i-1]
                    break

        segment_length = next_point.distance - cur_point.distance
        dist_past_cur = distance - cur_point.distance
        bias = dist_past_cur / segment_length

        dx = next_point.x - cur_point.x
        dy = next_point.y - cur_point.y

        return ContourPoint(cur_point.x + dx * bias, cur_point.y + dy * bias, distance)

def _distance(x1, y1, x2, y2) -> float:
    dx = x1 - x2
    dy = y1 - y2
    return math.sqrt(dx*dx + dy*dy)

