import math
import itertools
import re
from mylib.aoc_basics import Day


class PartA(Day):
    def parse(self, text, data):
        match = re.match(r".*x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)", text)
        if not match:
            raise RuntimeError("Invalid input")
        data.limits = [(int(match.group(1)),
                        int(match.group(2))),
                       (int(match.group(3)),
                        int(match.group(4)))]

    def compute(self, data):
        max_vy = int(-data.limits[1][0] - 1)
        return int(max_vy * (max_vy + 1) / 2)

    def example_answer(self):
        return 45


class PartB(PartA):
    def compute(self, data):
        min_vy = data.limits[1][0]
        max_vy = int(-data.limits[1][0] - 1)
        min_vx = int(.5 * math.sqrt(1 + 8 * data.limits[0][0]))
        max_vx = int(data.limits[0][1])
        velocities = list(itertools.product(range(min_vx, max_vx + 1), range(min_vy, max_vy + 1)))
        hits = [v for v in velocities if self.is_hit(v, data.limits)]
        return len(hits)

    @staticmethod
    def sign(x):
        if x < 0:
            return -1
        if x > 0:
            return 1
        return 0

    @classmethod
    def is_hit(cls, velocity, target):
        vx, vy = velocity
        x, y = 0, 0
        (x_min, x_max), (y_min, y_max) = target

        while True:
            x += vx
            y += vy

            vx -= cls.sign(vx)
            vy -= 1

            if x > x_max:
                return False
            if y < y_min:
                return False
            if x >= x_min and y <= y_max:
                return True

    def example_answer(self):
        return 112


Day.do_day(17, 2021, PartA, PartB)
