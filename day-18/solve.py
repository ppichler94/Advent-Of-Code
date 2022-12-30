from collections import namedtuple
from mylib.aoc_basics import Day


class Cube:
    def __init__(self, coordinates):
        self.x = int(coordinates[0])
        self.y = int(coordinates[1])
        self.z = int(coordinates[2])
        self.surface = 6

    def touches(self, cube):
        return abs(self.x - cube.x) + abs(self.y - cube.y) + abs(self.z - cube.z) == 1

    def __repr__(self):
        return f"Cube(x={self.x}, y={self.y}, z={self.z}, surface={self.surface})"


class PartA(Day):
    def parse(self, text, data):
        data.cubes = []
        for line in text.split("\n"):
            data.cubes.append(Cube(line.split(",")))

    def compute(self, data):
        grid = []
        for new_cube in data.cubes:
            for cube in grid:
                if cube.touches(new_cube):
                    cube.surface -= 1
                    new_cube.surface -= 1
            grid.append(new_cube)
        return sum(cube.surface for cube in grid)

    def example_answer(self):
        return 64


class PartB(Day):
    def example_answer(self):
        return 58


Day.do_day(18, 2022, PartA, PartB)
