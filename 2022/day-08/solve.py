import numpy as np
from mylib.aoc_basics import Day


class PartA(Day):
    def parse(self, text, data):
        data.trees = np.array([list(line) for line in text.splitlines()], dtype=int)

    def compute(self, data):
        visibility = np.zeros(data.trees.shape, dtype=bool)
        PartA.calculate_visibility_row(data.trees, visibility, 0, data.trees.shape[1], 1)
        PartA.calculate_visibility_row(data.trees, visibility, data.trees.shape[1] - 1, -1, -1)
        PartA.calculate_visibility_col(data.trees, visibility, 0, data.trees.shape[0], 1)
        PartA.calculate_visibility_col(data.trees, visibility, data.trees.shape[0] - 1, -1, -1)
        return np.count_nonzero(visibility)

    @staticmethod
    def calculate_visibility_row(trees, visibility, start, stop, step):
        for row in range(0, trees.shape[0]):
            current_height = -1
            for col in range(start, stop, step):
                if trees[row, col] > current_height:
                    visibility[row, col] |= True
                    current_height = trees[row, col]

    @staticmethod
    def calculate_visibility_col(trees, visibility, start, stop, step):
        for col in range(0, trees.shape[1]):
            current_height = -1
            for row in range(start, stop, step):
                if trees[row, col] > current_height:
                    visibility[row, col] |= True
                    current_height = trees[row, col]

    def example_answer(self):
        return 21


class PartB(PartA):
    def compute(self, data):
        scenic_score = PartB.calculate_scenic_scores(data.trees)
        return int(np.max(scenic_score))

    @staticmethod
    def calculate_scenic_scores(trees):
        score = np.zeros(trees.shape, dtype=int)
        for row in range(1, trees.shape[0] - 1):
            for col in range(1, trees.shape[1] - 1):
                score[row, col] = PartB.calculate_scenic_score(trees, row, col)
        return score

    @staticmethod
    def calculate_scenic_score(trees, row, col):
        up = PartB.calculate_scenic_score_col(trees, col, row, -1, -1)
        down = PartB.calculate_scenic_score_col(trees, col, row, trees.shape[0], 1)
        left = PartB.calculate_scenic_score_row(trees, row, col, -1, -1)
        right = PartB.calculate_scenic_score_row(trees, row, col, trees.shape[1], 1)
        return up * down * left * right

    @staticmethod
    def calculate_scenic_score_row(trees, row, start, stop, step):
        score = 0
        house_height = trees[row, start]
        for col in range(start + step, stop, step):
            score += 1
            if trees[row, col] >= house_height:
                return score
        return score

    @staticmethod
    def calculate_scenic_score_col(trees, col, start, stop, step):
        score = 0
        house_height = trees[start, col]
        for row in range(start + step, stop, step):
            score += 1
            if trees[row, col] >= house_height:
                return score
        return score

    def example_answer(self):
        return 8


Day.do_day(8, 2022, PartA, PartB)
