from operator import add, mul
from mylib.aoc_basics import Day
import pyparsing


class PartA(Day):
    def part_config(self, data):
        integer = pyparsing.Word(pyparsing.nums)
        op = pyparsing.one_of("+ *")
        data.expr = pyparsing.infix_notation(
            integer, [(op, 2, pyparsing.opAssoc.LEFT, self.action)], lpar="(", rpar=")"
        )

    @staticmethod
    def action(tokens):
        terms = tokens[0]
        while len(terms) >= 3:
            left = int(terms.pop(0))
            op = terms.pop(0)
            right = int(terms.pop(0))
            result = {"+": add, "*": mul}[op](left, right)
            terms.insert(0, str(result))
        return terms[0]

    def compute(self, data):
        return sum(self.evaluate_line(data, line) for line in data.text.splitlines())

    @staticmethod
    def evaluate_line(data, line):
        result = data.expr.parseString(line, parse_all=True)
        return int(result[0])

    def example_answer(self):
        return 71

    def get_example_input(self, puzzle):
        return "1 + 2 * 3 + 4 * 5 + 6"

    def tests(self):
        yield "2 * 3 + (4 * 5)", 26, "Example2"
        yield "5 + (8 * 3 + 9 + 3 * 4 * 3)", 437, "Example3"
        yield "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 12240, "Example4"
        yield "2 * 3 + (4 * 5)\n5 + (8 * 3 + 9 + 3 * 4 * 3)\n5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))\n((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 26335, "Combined Test"


class PartB(PartA):
    def part_config(self, data):
        integer = pyparsing.Word(pyparsing.nums)
        data.expr = pyparsing.infix_notation(
            integer,
            [
                ("+", 2, pyparsing.opAssoc.LEFT, self.action),
                ("*", 2, pyparsing.opAssoc.LEFT, self.action),
            ],
            lpar="(",
            rpar=")",
        )

    def example_answer(self):
        return 231

    def tests(self):
        yield "2 * 3 + (4 * 5)", 46, "Example2"
        yield "5 + (8 * 3 + 9 + 3 * 4 * 3)", 1445, "Example3"
        yield "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 669060, "Example4"
        yield "2 * 3 + (4 * 5)\n5 + (8 * 3 + 9 + 3 * 4 * 3)\n5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))\n((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 693891, "Combined Test"


Day.do_day(18, 2020, PartA, PartB)
