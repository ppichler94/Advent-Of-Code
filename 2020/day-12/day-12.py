import math
from mylib.aoc_basics import Day
import numpy as np


class PartA(Day):
    def parse(self, text, data):
        data.instructions = [
            (action, int(value)) for action, value in [(line[0], line[1:]) for line in text.splitlines()]
        ]

    def compute(self, data):
        x = 0
        y = 0
        direction = 0
        for instruction in data.instructions:
            match instruction:
                case ["N", int(units)]:
                    y -= units
                case ["S", int(units)]:
                    y += units
                case ["W", int(units)]:
                    x -= units
                case ["E", int(units)]:
                    x += units
                case ["L", int(degrees)]:
                    direction -= degrees
                case ["R", int(degrees)]:
                    direction += degrees
                case ["F", int(units)]:
                    x += int(units * math.cos(math.radians(direction)))
                    y += int(units * math.sin(math.radians(direction)))

        return abs(x) + abs(y)

    def example_answer(self):
        return 25


class PartB(PartA):
    def compute(self, data):
        ship = np.zeros(2)
        waypoint = np.array((-1, 10))
        for instruction in data.instructions:
            match instruction:
                case ["N", int(units)]:
                    waypoint += (-units, 0)
                case ["S", int(units)]:
                    waypoint += (units, 0)
                case ["W", int(units)]:
                    waypoint += (0, -units)
                case ["E", int(units)]:
                    waypoint += (0, units)
                case ["L", int(degrees)]:
                    waypoint = waypoint.dot(self.rotation(degrees))
                case ["R", int(degrees)]:
                    waypoint = waypoint.dot(self.rotation(-degrees))
                case ["F", int(units)]:
                    ship += units * waypoint

        return int(np.sum(np.abs(ship - np.array([0, 0]))))

    @staticmethod
    def rotation(degrees):
        return np.array([
            [math.cos(math.radians(degrees)), math.sin(math.radians(degrees))],
            [-math.sin(math.radians(degrees)), math.cos(math.radians(degrees))],
        ])

    def example_answer(self):
        return 286


Day.do_day(12, 2020, PartA, PartB)
