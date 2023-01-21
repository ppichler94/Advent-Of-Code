import functools
import operator
from mylib.aoc_basics import Day
import nographs as nog


class PartA(Day):
    def parse(self, text, data):
        data.trees = nog.Array(text.splitlines())
        data.limits = data.trees.limits()

    def compute(self, data):
        return self.count_trees(data, (1, 3))

    @staticmethod
    def count_trees(data, slope):
        pos = nog.Position.at(0, 0)
        tree_count = 0
        while True:
            pos = (pos + slope).wrap_to_cuboid(data.limits)
            if pos[0] < slope[0]:
                return tree_count
            if data.trees[pos] == "#":
                tree_count += 1

    def example_answer(self):
        return 7


class PartB(PartA):
    def compute(self, data):
        slopes = [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]
        return functools.reduce(operator.mul, [self.count_trees(data, slope) for slope in slopes])

    def example_answer(self):
        return 336


Day.do_day(3, 2020, PartA, PartB)
