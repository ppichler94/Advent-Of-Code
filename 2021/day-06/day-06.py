import numpy as np
from mylib.aoc_basics import Day


class PartA(Day):
    def parse(self, text, data):
        population = np.array([int(x) for x in text.split(",")])
        data.bins = np.array([(population == i).sum() for i in range(10)], dtype=np.longlong)

    def part_config(self, data):
        data.number_of_days = 80

    def compute(self, data):
        for _ in range(0, data.number_of_days):
            self.spawn_new(data)
            data.bins = np.roll(data.bins, -1)
        return int(data.bins.sum())

    @staticmethod
    def spawn_new(data):
        number_of_zeros = data.bins[0]
        data.bins[0] = 0
        data.bins[7] += number_of_zeros
        data.bins[9] += number_of_zeros

    def example_answer(self):
        return 5934


class PartB(PartA):
    def part_config(self, data):
        data.number_of_days = 256

    def example_answer(self):
        return 26984457539


Day.do_day(6, 2021, PartA, PartB)

