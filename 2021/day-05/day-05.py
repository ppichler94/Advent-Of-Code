import numpy as np

from mylib.aoc_basics import Day


class Field:
    def __init__(self, start_coordinates, end_coordinates, consider_diagonals):
        self.consider_diagonals = consider_diagonals
        self.start_coordinates = start_coordinates
        self.end_coordinates = end_coordinates
        self.width = 1 + max(self.start_coordinates[:, 0].max(), self.end_coordinates[:, 0].max())
        self.height = 1 + max(self.start_coordinates[:, 1].max(), self.end_coordinates[:, 1].max())
        self.data = np.zeros([self.height, self.width], dtype=int)
        self.add_lines()

    @classmethod
    def from_string(cls, text, consider_diagonals):
        start_coordinates = np.empty([len(text), 2], dtype=int)
        end_coordinates = np.empty([len(text), 2], dtype=int)
        for index, line in enumerate(text):
            coords = line.split(" -> ")
            start_coords = coords[0].split(",")
            end_coords = coords[1].split(",")
            start_coordinates[index, 0] = int(start_coords[0])
            start_coordinates[index, 1] = int(start_coords[1])
            end_coordinates[index, 0] = int(end_coords[0])
            end_coordinates[index, 1] = int(end_coords[1])
        return Field(start_coordinates, end_coordinates, consider_diagonals)

    def add_lines(self):
        for index in range(0, self.start_coordinates.shape[0]):
            start = self.start_coordinates[index]
            end = self.end_coordinates[index]
            if start[1] == end[1]:
                self.add_horizontal_line(start[1], start[0], end[0])
            elif start[0] == end[0]:
                self.add_vertical_line(start[0], start[1], end[1])
            elif self.consider_diagonals:
                self.add_diagonal_line(start, end)

    def add_horizontal_line(self, y, x1, x2):
        if x2 < x1:
            x1, x2 = x2, x1
        for x in range(x1, x2 + 1):
            self.data[y, x] += 1

    def add_vertical_line(self, x, y1, y2):
        if y2 < y1:
            y1, y2 = y2, y1
        for y in range(y1, y2 + 1):
            self.data[y, x] += 1

    def add_diagonal_line(self, start, end):
        dir_x = 1 if start[0] < end[0] else -1
        dir_y = 1 if start[1] < end[1] else -1
        x1, x2 = start[0], end[0]
        y1 = start[1]
        while True:
            self.data[y1, x1] += 1
            x1 += dir_x
            y1 += dir_y
            if x1 == x2 + dir_x:
                break

    def get_number_of_overlaps(self):
        return self.data[self.data > 1].size


class PartA(Day):
    def parse(self, text, data):
        data.data = Field.from_string(text.splitlines(), False)

    def compute(self, data):
        return data.data.get_number_of_overlaps()

    def example_answer(self):
        return 5


class PartB(Day):
    def parse(self, text, data):
        data.data = Field.from_string(text.splitlines(), True)

    def compute(self, data):
        return data.data.get_number_of_overlaps()

    def example_answer(self):
        return 12


Day.do_day(5, 2021, PartA, PartB)

