from abc import ABC
from dataclasses import dataclass
from itertools import product
from typing import Tuple

from mylib.aoc_basics import Day


class Segment(ABC):
    def intersect(self, segment):
        ...

    @classmethod
    def of_points(cls, point1, point2):
        if point1[1] == point2[1]:
            return VerticalSegment(point1[1], min(point1[0], point2[0]), max(point1[0], point2[0]))
        if point1[0] == point2[0]:
            return HorizontalSegment(min(point1[1], point2[1]), max(point1[1], point2[1]), point1[0])


@dataclass
class HorizontalSegment(Segment):
    x1: int
    x2: int
    y: int

    def intersect(self, segment):
        if type(segment) is not VerticalSegment:
            return None

        if self.x1 <= segment.x <= self.x2 and segment.y1 <= self.y <= segment.y2:
            return self.y, segment.x
        return None


@dataclass
class VerticalSegment(Segment):
    x: int
    y1: int
    y2: int

    def intersect(self, segment):
        if type(segment) is not HorizontalSegment:
            return None
        if segment.x1 <= self.x <= segment.x2 and self.y1 <= segment.y <= self.y2:
            return segment.y, self.x
        return None


class PartA(Day):
    def parse(self, text, data):
        wire1_path, wire2_path = text.splitlines()
        data.wire1_segments = self.path_to_segments(wire1_path)
        data.wire2_segments = self.path_to_segments(wire2_path)

    @staticmethod
    def path_to_segments(path):
        segments = []
        pos = (0, 0)
        for instruction in path.split(","):
            distance = int(instruction[1:])
            match (instruction[0]):
                case "U":
                    next_pos = (pos[0] + distance, pos[1])
                case "R":
                    next_pos = (pos[0], pos[1] + distance)
                case "D":
                    next_pos = (pos[0] - distance, pos[1])
                case "L":
                    next_pos = (pos[0], pos[1] - distance)
            segments.append(Segment.of_points(pos, next_pos))
            pos = next_pos
        return segments

    def compute(self, data):
        intersections = []
        for segment1, segment2 in product(data.wire1_segments, data.wire2_segments):
            if intersection := segment1.intersect(segment2):
                intersections.append(intersection)

        return min(self.distance_to_origin(data, point) for point in intersections if point != (0, 0))

    def distance_to_origin(self, data, point):
        return abs(point[0]) + abs(point[1])

    def get_example_input(self, puzzle):
        return None

    def tests(self):
        yield "R8,U5,L5,D3\nU7,R6,D4,L4", 6, "Example1"
        yield "R75,D30,R83,U83,L12,D49,R71,U7,L72\nU62,R66,U55,R34,D71,R55,D58,R83", 159, "Example2"
        yield "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\nU98,R91,D20,R16,D67,R40,U7,R15,U6,R7", 135, "Example3"


class PartB(PartA):
    def distance_to_origin(self, data, point):
        distance1 = self.find_distance(data.wire1_segments, point)
        distance2 = self.find_distance(data.wire2_segments, point)
        return distance1 + distance2

    @staticmethod
    def find_distance(segments, point):
        distance = 0
        pos = (0, 0)
        for segment in segments:
            match segment:
                case HorizontalSegment(x1, x2, y):
                    if x1 <= point[1] <= x2 and y == point[0]:
                        return distance + abs(point[1] - pos[1])
                    else:
                        distance += abs(x2 - x1)
                        pos = (pos[0], x2 if pos[1] == x1 else x1)
                case VerticalSegment(x, y1, y2):
                    if x == point[1] and y1 <= point[0] <= y2:
                        return distance + abs(point[0] - pos[0])
                    else:
                        distance += abs(y2 - y1)
                        pos = (y2 if pos[0] == y1 else y1, pos[1])
        raise RuntimeError("intersection not found")

    def tests(self):
        yield "R8,U5,L5,D3\nU7,R6,D4,L4", 30, "Example1"
        yield "R75,D30,R83,U83,L12,D49,R71,U7,L72\nU62,R66,U55,R34,D71,R55,D58,R83", 610, "Example2"
        yield "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\nU98,R91,D20,R16,D67,R40,U7,R15,U6,R7", 410, "Example3"


Day.do_day(3, 2019, PartA, PartB)
