import numpy as np
import re
from mylib.aoc_basics import Day


class PartA(Day):
    def parse(self, text, data):
        numbers_text, *boards_text = text.split("\n\n")
        data.numbers = [int(x) for x in numbers_text.split(",")]
        data.boards = [np.array([x for x in [re.findall(r"\d+", line) for line in block.splitlines()]], dtype=int)
                       for block in boards_text]
        data.marked_boards = [np.zeros([5, 5], dtype=int) for _ in range(len(data.boards))]

    def compute(self, data):
        for number in data.numbers:
            for board, marked_board in zip(data.boards, data.marked_boards):
                index = np.where(board == number)
                marked_board[index] = 1
                winning_board = self.check_winning_condition(marked_board, index)
                if winning_board:
                    return self.calculate_points(board, marked_board, number)
        return 0

    @staticmethod
    def check_winning_condition(marked_board, mark_index):
        column_sum = np.sum(marked_board, axis=0)[mark_index[1]]
        row_sum = np.sum(marked_board, axis=1)[mark_index[0]]
        if ((column_sum.size > 0 and column_sum == 5)
            or (row_sum.size > 0 and row_sum == 5)):
            return True
        return False

    @staticmethod
    def calculate_points(board, marked_board, number):
        unmarked = np.ma.array(board, mask=marked_board)
        sum_of_unmarked = unmarked.sum()
        return int(sum_of_unmarked * number)

    def example_answer(self):
        return 4512


class PartB(PartA):
    def compute(self, data):
        last_winning_board = np.empty([5, 5])
        last_winning_marks = np.empty([5, 5])
        last_number = 0
        winning_indices = []

        for number in data.numbers:
            for i, (board, marked_board) in enumerate(zip(data.boards, data.marked_boards)):
                if i in winning_indices:
                    continue
                index = np.where(board == number)
                marked_board[index] = 1
                winning_board = self.check_winning_condition(marked_board, index)
                if winning_board:
                    winning_indices.append(i)
                    last_winning_board = board
                    last_winning_marks = marked_board
                    last_number = number

        return self.calculate_points(last_winning_board, last_winning_marks, last_number)

    def example_answer(self):
        return 1924


Day.do_day(4, 2021, PartA, PartB)
