import re
from collections import namedtuple


def main():
    example_data = read_input_from_file("example.txt")
    input_data = read_input_from_file("input.txt")

    print(f'Result example A: {solve_a(example_data, 10)}\n')
    print(f'Result puzzle data A: {solve_a(input_data, 2000000)}\n')
    print(f'Result example B: {solve_b(example_data)}\n')
    print(f'Result puzzle data B: {solve_b(input_data)}\n')


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


def solve_b(input):
    return


if __name__ == "__main__":
    main()
