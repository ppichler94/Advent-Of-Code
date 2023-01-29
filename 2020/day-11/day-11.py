from functools import partial

from mylib.aoc_basics import Day
import nographs as nog


class PartA(Day):
    def parse(self, text, data):
        data.array = nog.Array([list(line) for line in text.splitlines()])
        data.limits = data.array.limits()
        data.moves = nog.Position.moves(diagonals=True)

    def compute(self, data):
        while True:
            empty_seats = data.array.findall("L")
            filled_seats = data.array.findall("#")
            to_fill = list(filter(partial(self.filter_empty, data), empty_seats))
            to_empty = list(filter(partial(self.filter_filled_seats, data), filled_seats))
            for seat in to_fill:
                data.array[seat] = "#"
            for seat in to_empty:
                data.array[seat] = "L"
            if len(to_fill) == 0 and len(to_empty) == 0:
                return len(filled_seats)

    def filter_empty(self, data, seat):
        return self.count_occupied_neighbors(data, seat) == 0

    def filter_filled_seats(self, data, seat):
        return self.count_occupied_neighbors(data, seat) >= 4

    @staticmethod
    def count_occupied_neighbors(data, pos):
        return sum(data.array[neighbor] == "#" for neighbor in pos.neighbors(data.moves, data.limits))

    def example_answer(self):
        return 37


class PartB(PartA):
    def filter_empty(self, data, seat):
        return self.count_visible_occupied_seats(data, seat) == 0

    def filter_filled_seats(self, data, seat):
        return self.count_visible_occupied_seats(data, seat) >= 5

    def count_visible_occupied_seats(self, data, pos):
        return sum(1 if self.is_occupied_seat_visible(data, pos, direction) else 0 for direction in data.moves)

    @staticmethod
    def is_occupied_seat_visible(data, pos, direction):
        current_pos = pos + direction
        while True:
            if not current_pos.is_in_cuboid(data.limits):
                return False
            if data.array[current_pos] == "#":
                return True
            if data.array[current_pos] == "L":
                return False
            current_pos = current_pos + direction

    def example_answer(self):
        return 26


Day.do_day(11, 2020, PartA, PartB)
