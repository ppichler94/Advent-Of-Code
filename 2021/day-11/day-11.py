import itertools
import nographs as nog
import numpy as np
from mylib.aoc_basics import Day


class PartA(Day):
    def parse(self, text, data):
        data.energy_levels = np.array([[int(x) for x in line] for line in text.splitlines()], dtype=int)
        data.moves = nog.Position.moves(diagonals=True)
        data.limits = ((0, data.energy_levels.shape[0]), (0, data.energy_levels.shape[1]))

    def compute(self, data):
        return sum(self.step(data) for _ in range(100))

    @staticmethod
    def step(data):
        flashed = set()
        data.energy_levels += 1
        flashing = np.argwhere(data.energy_levels > 9)
        while len(flashing):
            flashing = list(filter(lambda x: x not in flashed,
                                   [nog.Position(x) for x in np.argwhere(data.energy_levels > 9)]))
            flashed.update(flashing)
            increasing = list(itertools.chain.from_iterable(nog.Position(x).neighbors(data.moves, data.limits)
                                                            for x in flashing))
            for y, x in increasing:
                data.energy_levels[y, x] += 1
        for y, x in flashed:
            data.energy_levels[y, x] = 0
        return len(flashed)

    def example_answer(self):
        return 1656


class PartB(PartA):
    def compute(self, data):
        for steps in itertools.count(1):
            self.step(data)
            if np.all(data.energy_levels == 0):
                break
        return steps

    def example_answer(self):
        return 195


Day.do_day(11, 2021, PartA, PartB)
