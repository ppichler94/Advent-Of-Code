import numpy as np
from mylib.aoc_basics import Day
import re


class PartA(Day):
    def parse(self, text, data):
        points_text, commands_text = text.split("\n\n")
        data.commands = [x for x in self.generate_commands(text.splitlines())]

        points = [tuple(int(x) for x in line.split(",")) for line in points_text.splitlines()]
        x = max(point[0] for point in points) + 1
        y = max(point[1] for point in points) + 1
        data.paper = np.zeros((y, x))

        for point in points:
            data.paper[point[1], point[0]] = 1

    @staticmethod
    def generate_commands(lines):
        for line in lines:
            if match := re.match(r".*([yx])=(\d+)", line):
                yield match.group(1), int(match.group(2))

    def compute(self, data):
        data.commands = [data.commands[0]]
        self.do_folds(data)
        return np.count_nonzero(data.paper)

    @staticmethod
    def do_folds(data):
        for command in data.commands:
            match command:
                case ["y", y]:
                    upper = data.paper[0:y, :]
                    lower = np.zeros(upper.shape)
                    lower[-(data.paper.shape[0] - y - 1):, :] = np.flipud(data.paper[y + 1:data.paper.shape[0], :])
                    data.paper = upper + lower
                case ["x", x]:
                    left = data.paper[:, 0:x]
                    right = np.zeros(left.shape)
                    right[:, -(data.paper.shape[1] - x - 1):] = np.fliplr(data.paper[:, x + 1:data.paper.shape[1]])
                    data.paper = left + right

    def example_answer(self):
        return 17

    def get_example_input(self, puzzle):
        return """
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
"""


class PartB(PartA):
    def compute(self, data):
        self.do_folds(data)
        for row in data.paper:
            print("".join([" " if x == 0 else "#" for x in row]))
        return None

    def example_answer(self):
        return None


Day.do_day(13, 2021, PartA, PartB)
