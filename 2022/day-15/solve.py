import re
from collections import namedtuple
from mylib.aoc_basics import Day


Beacon = namedtuple("Beacon", ["x", "y"])


class Sensor:
    def __init__(self, x, y, closest_beacon):
        self.x = x
        self.y = y
        self.closest_beacon = closest_beacon
        self.beacon_radius = abs(self.x - closest_beacon.x) + abs(self.y - closest_beacon.y)

    def coverage_at_y_level(self, y_level):
        coverage = self.beacon_radius - abs(self.y - y_level)
        if coverage > 0:
            return [self.x - coverage, self.x + coverage]

    @classmethod
    def from_text(cls, line):
        matcher = re.search("Sensor at x=(.*), y=(.*): closest beacon is at x=(.*), y=(.*)", line)
        return cls(int(matcher.group(1)), int(matcher.group(2)), Beacon(int(matcher.group(3)), int(matcher.group(4))))


class PartA(Day):
    def parse(self, text, data):
        data.sensors = [Sensor.from_text(line) for line in text.splitlines()]

    def compute(self, data):
        y_level = 2000000 if data.config is None else 10
        coverages = [sensor.coverage_at_y_level(y_level) for sensor in data.sensors]
        return self.count_covered_positions(coverages)

    @staticmethod
    def count_covered_positions(coverages):
        covered = set()
        for coverage in coverages:
            if coverage:
                covered.update(range(coverage[0], coverage[1]))
        return len(covered)

    def example_answer(self):
        return 26


class PartB(PartA):
    def compute(self, data):
        x_max = 4000000 if data.config is None else 20
        y_max = x_max
        for y_level in range(y_max):
            coverages = [sensor.coverage_at_y_level(y_level) for sensor in data.sensors]
            coverages = self.merge_coverages(coverages)
            for coverage in coverages:
                if coverage[0] > 0:
                    return y_level + (coverage[0] - 1) * 4000000
                if coverage[1] < x_max:
                    return y_level + (coverage[1] + 1) * 4000000

    @staticmethod
    def merge_coverages(coverages):
        if len(coverages) == 0 or len(coverages) == 1:
            return coverages
        coverages = [c for c in coverages if c]
        coverages.sort(key=lambda c: c[0])
        result = [coverages[0]]
        for interval in coverages[1:]:
            if interval[0] <= result[-1][1]:
                result[-1][1] = max(result[-1][1], interval[1])
            else:
                result.append(interval)
        return result

    def example_answer(self):
        return 56000011


Day.do_day(15, 2022, PartA, PartB)
