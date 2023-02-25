from itertools import product
from operator import add, mul
from mylib.aoc_basics import Day


class PartA(Day):
    def parse(self, text, data):
        data.program = [int(x) for x in text.split(",")]

    def compute(self, data):
        if data.config is None:
            data.program[1] = 12
            data.program[2] = 2
        return self.execute_program(data.program)

    @staticmethod
    def execute_program(program):
        pc = 0
        while True:
            instruction = program[pc]
            match instruction:
                case 1:
                    op = add
                case 2:
                    op = mul
                case 99:
                    break
                case _:
                    raise RuntimeError(f"Invalid instruction {instruction} at position {pc}")

            pos1 = program[pc + 1]
            pos2 = program[pc + 2]
            result_pos = program[pc + 3]
            arg1 = program[pos1]
            arg2 = program[pos2]
            result = op(arg1, arg2)
            program[result_pos] = result
            pc += 4

        return program[0]

    def example_answer(self):
        return 3500

    def tests(self):
        yield "1,0,0,0,99", 2, "Example1"
        yield "2,3,0,3,99", 2, "Example2"
        yield "2,4,4,5,99,0", 2, "Example3"
        yield "1,1,1,4,99,5,6,0,99", 30, "Example4"


class PartB(PartA):
    def compute(self, data):
        for noun, verb in product(range(0, 99), repeat=2):
            program = list(data.program)
            program[1] = noun
            program[2] = verb
            if self.execute_program(program) == 19690720:
                return 100 * noun + verb
        return "No result"

    def get_example_input(self, puzzle):
        return None

    def tests(self):
        return []


Day.do_day(2, 2019, PartA, PartB)
