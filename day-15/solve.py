import itertools
import re
from collections import namedtuple


def main():
    example_data = read_input_from_file("example.txt")
    input_data = read_input_from_file("input.txt")

    print(f'Result example A: {solve_a(example_data, 10)}\n')
    print(f'Result puzzle data A: {solve_a(input_data, 2000000)}\n')
    print(f'Result example B: {solve_b(example_data, 20, 20)}\n')
    print(f'Result puzzle data B: {solve_b(input_data, 4000000, 4000000)}\n')


Beacon = namedtuple("Beacon", ["x", "y"])


class Sensor:
    def __init__(self, x, y, closest_beacon):
        self.x = x
        self.y = y
        self.closest_beacon = closest_beacon
        self.beacon_radius = abs(self.x - closest_beacon.x) + abs(self.y - closest_beacon.y)

    def coverage_at_y_level(self, y_level):
        coverage = self.beacon_radius -  abs(self.y - y_level)
        if coverage > 0:
            return [self.x - coverage, self.x + coverage]


def read_input_from_file(file_name):
    input_file = open(file_name, "r")
    data = input_file.readlines()
    input_file.close()
    data = [x.strip() for x in data]
    return data


def solve_a(input, y_level):
    sensors = parse_input(input)
    coverages = [sensor.coverage_at_y_level(y_level) for sensor in sensors]
    return count_covered_positions(coverages)


def parse_input(input):
    sensors = []
    for line in input:
        matcher = re.search("Sensor at x=(.*), y=(.*): closest beacon is at x=(.*), y=(.*)", line)
        if matcher:
            sensors.append(Sensor(int(matcher.group(1)), int(matcher.group(2)), Beacon(int(matcher.group(3)), int(matcher.group(4)))))
    return sensors


def count_covered_positions(coverages):
    covered = set()
    for coverage in coverages:
        if coverage:
            covered.update(range(coverage[0], coverage[1]))
    return len(covered)


def solve_b(input, x_max, y_max):
    sensors = parse_input(input)
    for y_level in range(y_max):
        coverages = [sensor.coverage_at_y_level(y_level) for sensor in sensors]
        coverages = merge_coverages(coverages)
        for coverage in coverages:
            if coverage[0] > 0:
                return y_level + (coverage[0] - 1) * 4000000
            if coverage[1] < x_max:
                return y_level + (coverage[1] + 1) * 4000000


def merge_coverages(coverages):
    if len(coverages) == 0 or len(coverages) == 1:
        return coverages
    coverages = [c for c in coverages if c]
    coverages.sort(key=lambda c:c[0])
    result = [coverages[0]]
    for interval in coverages[1:]:
        if interval[0] <= result[-1][1]:
            result[-1][1] = max(result[-1][1], interval[1])
        else:
            result.append(interval)
    return result


if __name__ == "__main__":
    main()
