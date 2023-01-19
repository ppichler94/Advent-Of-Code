import re
from mylib.aoc_basics import Day


class PartA(Day):
    def parse(self, text, data):
        data.lines = [self.parse_line(line) for line in text.splitlines()]

    @staticmethod
    def parse_line(line):
        matcher = re.match(r"(\d+)-(\d+) ([a-z]): (\w+)", line)
        return int(matcher.group(1)), int(matcher.group(2)), matcher.group(3), matcher.group(4)

    def compute(self, data):
        return sum(
            1 if password.count(character) in range(start, stop + 1) else 0
            for start, stop, character, password in data.lines
        )

    def example_answer(self):
        return 2


class PartB(PartA):
    def compute(self, data):
        return sum(
            1 if bool(password[start - 1] == character) != bool(password[end - 1] == character) else 0
            for start, end, character, password in data.lines
        )

    def example_answer(self):
        return 1


Day.do_day(2, 2020, PartA, PartB)
