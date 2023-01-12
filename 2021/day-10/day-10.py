import statistics
from mylib.aoc_basics import Day


class PartA(Day):
    def parse(self, text, data):
        data.lines = text.splitlines()

    def compute(self, data):
        return sum(self.get_points_for_line(line) for line in data.lines)

    @staticmethod
    def check_character(character, stack):
        matching_character = {"(": ")", "[": "]", "{": "}", "<": ">"}
        if character in ["(", "[", "{", "<"]:
            stack.append(character)
        else:
            last_character = stack.pop()
            required_character = matching_character[last_character]
            if character != required_character:
                return False
        return True

    def get_points_for_line(self, line):
        point_table = {")": 3, "]": 57, "}": 1197, ">": 25137}
        stack = []
        for character in line:
            matching = self.check_character(character, stack)
            if not matching:
                return point_table[character]
        return 0

    def example_answer(self):
        return 26397

    def get_example_input(self, puzzle):
        return """
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
"""


class PartB(PartA):
    def compute(self, data):
        lines = filter(self.is_not_corrupt, data.lines)
        points = [self.get_points_to_finish_line(line) for line in lines]
        return statistics.median(points)

    def is_not_corrupt(self, line):
        return self.get_points_for_line(line) == 0

    def get_points_to_finish_line(self, line):
        point_table = {"(": 1, "[": 2, "{": 3, "<": 4}
        stack = []
        for character in line:
            self.check_character(character, stack)
        points = 0
        stack.reverse()
        for c in stack:
            points = points * 5 + point_table[c]
        return points

    def example_answer(self):
        return 288957


Day.do_day(10, 2021, PartA, PartB)
