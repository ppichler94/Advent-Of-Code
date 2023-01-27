from functools import reduce
from itertools import product
from operator import mul
from mylib.aoc_basics import Day
import nographs as nog


class PartA(Day):
    def parse(self, text, data):
        data.trees = nog.Array([[int(x) for x in list(line)] for line in text.splitlines()])
        data.limits = data.trees.limits()

    def compute(self, data):
        visible = set()
        for y in range(data.limits[0][1]):
            visible.update(self.calculate_visiblility_line(data, nog.Position.at(y, 0), (0, 1)))
            visible.update(self.calculate_visiblility_line(data, nog.Position.at(y, data.limits[1][1] - 1), (0, -1)))
        for x in range(data.limits[1][1]):
            visible.update(self.calculate_visiblility_line(data, nog.Position.at(0, x), (1, 0)))
            visible.update(self.calculate_visiblility_line(data, nog.Position.at(data.limits[0][1] - 1, x), (-1, 0)))
        return len(visible)

    @staticmethod
    def calculate_visiblility_line(data, pos, direction):
        current_pos = pos
        current_height = -1
        visible = set()
        while current_pos.is_in_cuboid(data.limits):
            if data.trees[current_pos] > current_height:
                visible.add(current_pos)
                current_height = data.trees[current_pos]
            current_pos = current_pos + direction
        return visible

    def example_answer(self):
        return 21


class PartB(PartA):
    def compute(self, data):
        return max(
            self.calculate_scenic_score(data, nog.Position.at(y, x))
            for y, x in product(range(1, data.limits[0][1] - 1), range(1, data.limits[1][1] - 1))
        )

    def calculate_scenic_score(self, data, pos):
        directions = ((-1, 0), (1, 0), (0, -1), (0, 1))
        return reduce(mul, [self.calculate_score_line(data, pos, direction) for direction in directions])

    @staticmethod
    def calculate_score_line(data, pos, direction):
        current_pos = pos + direction
        score = 0
        while current_pos.is_in_cuboid(data.limits):
            score += 1
            if data.trees[current_pos] >= data.trees[pos]:
                break
            current_pos = current_pos + direction
        return score

    def example_answer(self):
        return 8


Day.do_day(8, 2022, PartA, PartB)
