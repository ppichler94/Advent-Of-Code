import functools
import itertools
import operator
import re
from mylib.aoc_basics import Day


class PartA(Day):
    def parse(self, text, data):
        data.numbers = list(map(int, re.findall(r"\d+", text)))
        data.sum_size = 2

    def compute(self, data):
        result = [x for x in itertools.permutations(data.numbers, data.sum_size) if sum(x) == 2020]
        if not result:
            raise RuntimeError("No pair sums to 2020")
        return functools.reduce(operator.mul, result[0])

    def example_answer(self):
        return 514579


class PartB(PartA):
    def part_config(self, data):
        data.sum_size = 3

    def example_answer(self):
        return 241861950


Day.do_day(1, 2020, PartA, PartB)
