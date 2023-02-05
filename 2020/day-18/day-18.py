import operator
from mylib.aoc_basics import Day
import pyparsing


class PartA(Day):
    def __init__(self):
        self.stack = []
        integer = pyparsing.Word(pyparsing.nums).setParseAction(self.add_to_stack)
        op = pyparsing.one_of("+ *")
        left_par, right_par = map(pyparsing.Suppress, "()")

        expr = pyparsing.Forward()
        atom = integer | pyparsing.Group(left_par + expr + right_par)
        expr <<= atom + (op + atom).setParseAction(self.add_to_stack)[...]
        self.expr = expr

    def compute(self, data):
        return sum(self.evaluate_line(line) for line in data.text.splitlines())

    def evaluate_line(self, line):
        self.stack[:] = []
        self.expr.parseString(line, parse_all=True)
        return self.evaluate_stack(self.stack[::-1])

    def add_to_stack(self, results: pyparsing.ParseResults):
        self.stack.append(results[0])

    def evaluate_stack(self, stack):
        next_element = stack.pop(0)
        if next_element in ["+", "*"]:
            operand2 = self.evaluate_stack(stack)
            operand1 = self.evaluate_stack(stack)
            return {"+": operator.add, "*": operator.mul}[next_element](operand1, operand2)
        else:
            return int(next_element)

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
    def __init__(self):
        self.stack = []
        integer = pyparsing.Word(pyparsing.nums).setParseAction(self.add_to_stack)
        left_par, right_par = map(pyparsing.Suppress, "()")

        expr = pyparsing.Forward()
        atom = integer | pyparsing.Group(left_par + expr + right_par)
        term = atom + ("+" + atom).setParseAction(self.add_to_stack)[...]
        expr <<= term + ("*" + term).setParseAction(self.add_to_stack)[...]
        self.expr = expr

    def example_answer(self):
        return 231

    def tests(self):
        yield "2 * 3 + (4 * 5)", 46, "Example2"
        yield "5 + (8 * 3 + 9 + 3 * 4 * 3)", 1445, "Example3"
        yield "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 669060, "Example4"
        yield "2 * 3 + (4 * 5)\n5 + (8 * 3 + 9 + 3 * 4 * 3)\n5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))\n((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 693891, "Combined Test"


Day.do_day(18, 2020, PartA, PartB)
