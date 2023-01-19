import re
from mylib.aoc_basics import Day


def cube_intersections(cube, cubes):
    cube_from, cube_to = cube
    for other in cubes:
        other_from, other_to = other
        intersection_from = tuple(map(max, zip(cube_from, other_from)))
        intersection_to = tuple(map(min, zip(cube_to, other_to)))
        if all(c_from <= c_to for c_from, c_to in zip(intersection_from, intersection_to)):
            yield intersection_from, intersection_to


class PartA(Day):
    def parse(self, text, data):
        data.lines = []
        for line in text.splitlines():
            cmd = line[0:3]
            xf, xt, yf, yt, zf, zt = (int(n) for n in re.findall(r"-?\d+", line))
            data.lines.append((cmd, ((xf, yf, zf), (xt, yt, zt))))
        data.limit = 50

    def compute(self, data):
        cubes = []
        cubes_negative = []

        for cmd, cube in data.lines:
            cube_from, cube_to = cube
            if data.limit and (any(c < -data.limit for c in cube_from) or any(c > data.limit for c in cube_to)):
                continue

            new_cubes_negative = list(cube_intersections(cube, cubes))
            new_cubes = list(cube_intersections(cube, cubes_negative))
            if cmd == "on ":
                new_cubes.append(cube)
            cubes.extend(new_cubes)
            cubes_negative.extend(new_cubes_negative)

        return (sum((xt - xf + 1) * (yt - yf + 1) * (zt - zf + 1)
                    for (xf, yf, zf), (xt, yt, zt) in cubes)
                -
                sum((xt - xf + 1) * (yt - yf + 1) * (zt - zf + 1)
                    for (xf, yf, zf), (xt, yt, zt) in cubes_negative))

    def example_answer(self):
        return 39


class PartB(PartA):
    def part_config(self, data):
        data.limit = None

    def example_answer(self):
        return None


Day.do_day(22, 2021, PartA, PartB)
