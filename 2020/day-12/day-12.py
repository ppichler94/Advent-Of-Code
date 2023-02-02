import math
from mylib.aoc_basics import Day
import numpy as np


class PartA(Day):
    def parse(self, text, data):
        data.instructions = [
            (action, int(value)) for action, value in [(line[0], line[1:]) for line in text.splitlines()]
        ]
        data.ship = np.zeros(2)
        data.waypoint = np.array([0, 1])

    def compute(self, data):
        for command, units in data.instructions:
            if command in "NSWE":
                self.move(data, command, units)
            elif command in "LR":
                data.waypoint = data.waypoint.dot(self.rotation(units * {"L": 1, "R": -1}[command]))
            elif command == "F":
                data.ship += units * data.waypoint

        return int(np.sum(np.abs(data.ship)))

    def move(self, data, direction, units):
        data.ship += units * np.array({"N": [-1, 0], "S": [1, 0], "W": [0, -1], "E": [0, 1]}[direction])

    @staticmethod
    def rotation(degrees):
        return np.array([
            [math.cos(math.radians(degrees)), math.sin(math.radians(degrees))],
            [-math.sin(math.radians(degrees)), math.cos(math.radians(degrees))],
        ], dtype=int)

    def example_answer(self):
        return 25


class PartB(PartA):
    def part_config(self, data):
        data.waypoint = np.array((-1, 10))

    def move(self, data, direction, units):
        data.waypoint += units * np.array({"N": [-1, 0], "S": [1, 0], "W": [0, -1], "E": [0, 1]}[direction])

    def example_answer(self):
        return 286


Day.do_day(12, 2020, PartA, PartB)
