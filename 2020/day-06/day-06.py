import re

from mylib.aoc_basics import Day


class PartA(Day):
    def compute(self, data):
        return sum(len(set(re.findall("[a-z]", group))) for group in data.text.split("\n\n"))

    def example_answer(self):
        return 11

    def get_example_input(self, puzzle):
        return """
abc

a
b
c

ab
ac

a
a
a
a

b
"""


class PartB(PartA):
    def compute(self, data):
        return sum(
            len(set.intersection(*[set(line) for line in group.splitlines()])) for group in data.text.split("\n\n")
        )

    def example_answer(self):
        return 6


Day.do_day(6, 2020, PartA, PartB)
