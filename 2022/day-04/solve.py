from mylib.aoc_basics import Day
import re


class PartA(Day):
    def parse(self, text, data):
        data.sections = [tuple(int(x) for x in re.findall(r"\d+", line)) for line in text.splitlines()]

    def compute(self, data):
        return sum(1 if (start1 <= start2 and end1 >= end2) or (start2 <= start1 and end2 >= end1)
                   else 0
                   for start1, end1, start2, end2 in data.sections)


class PartB(PartA):
    def compute(self, data):
        return sum(1 if PartB.overlaps(start1, end1, start2, end2) else 0
                   for start1, end1, start2, end2 in data.sections)

    @classmethod
    def overlaps(cls, start1, end1, start2, end2):
        if start2 <= start1 <= end2:
            return True
        if start2 <= end1 <= end2:
            return True
        if start1 <= start2 <= end1:
            return True
        if start1 <= end2 <= end1:
            return True
        return False


Day.do_day(4, 2022, PartA, PartB)
