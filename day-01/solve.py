import re

from mylib.aoc_basics import Day


class PartA(Day):
    def parse(self, text, data):
        data.calories_per_elf = [sum(int(i) for i in re.findall("\d+", block)) for block in text.split("\n\n")]

    def compute(self, data):
        return max(data.calories_per_elf)

    def tests(self):
        yield self.test_solve('''
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
        '''), 24000, "example"


class PartB(Day):

    def parse(self, text, data):
        data.calories_per_elf = [sum(int(i) for i in re.findall("\d+", block)) for block in text.split("\n\n")]

    def compute(self, data):
        calories_per_elf = sorted(data.calories_per_elf)
        return sum(calories_per_elf[-3:])

    def tests(self):
        yield self.test_solve('''
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
        '''), 45000, "example"

Day.do_day(1, 2022, PartA, PartB)
