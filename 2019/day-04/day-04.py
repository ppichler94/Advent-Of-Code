from collections import Counter
from itertools import pairwise
from mylib.aoc_basics import Day


class PartA(Day):
    def parse(self, text, data):
        min_text, max_text = text.split("-")
        data.min = int(min_text)
        data.max = int(max_text)

    def compute(self, data):
        return sum(self.is_valid(x) for x in range(data.min, data.max + 1))

    def is_valid(self, x):
        text = str(x)
        counts = Counter(text)
        if not any(count > 1 for count in counts.values()):
            return False
        if any(x1 > x2 for x1, x2 in pairwise(text)):
            return False
        return True


class PartB(PartA):
    def is_valid(self, x):
        text = str(x)
        counts = Counter(text)
        if not any(count == 2 for count in counts.values()):
            return False
        if any(x1 > x2 for x1, x2 in pairwise(text)):
            return False
        return True


Day.do_day(4, 2019, PartA, PartB)
