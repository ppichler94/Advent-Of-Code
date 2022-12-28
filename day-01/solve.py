import re

from mylib.aoc_basics import Day


class PartA(Day):
    def parse(self, text, data):
        data.calories_per_elf = [sum(int(i) for i in re.findall("\d+", block)) for block in text.split("\n\n")]

    def compute(self, data):
        return max(data.calories_per_elf)

    def example_answer(self):
        return 24000


class PartB(PartA):
    def compute(self, data):
        calories_per_elf = sorted(data.calories_per_elf)
        return sum(calories_per_elf[-3:])

    def example_answer(self):
        return 45000


Day.do_day(1, 2022, PartA, PartB)
