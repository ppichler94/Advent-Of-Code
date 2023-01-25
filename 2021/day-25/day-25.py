import itertools
from mylib.aoc_basics import Day
import nographs as nog


class PartA(Day):
    def parse(self, text, data):
        data.seafloor = nog.Array([list(line) for line in text.splitlines()])
        data.limits = data.seafloor.limits()
        data.moves = {">": (0, 1), "v": (1, 0)}

    def compute(self, data):
        for steps in itertools.count(1):
            moving = self.move(data, ">")
            moving |= self.move(data, "v")
            if not moving:
                return steps

    @staticmethod
    def move(data, direction):
        moving = False
        next_seafloor = data.seafloor.mutable_copy()
        east_facing = data.seafloor.findall(direction)
        for cucumber in east_facing:
            target = (cucumber + data.moves[direction]).wrap_to_cuboid(data.limits)
            if data.seafloor[target] == ".":
                next_seafloor[cucumber] = "."
                next_seafloor[target] = direction
                moving = True
        data.seafloor = next_seafloor
        return moving

    def example_answer(self):
        return 58


Day.do_day(25, 2021, PartA, None)
