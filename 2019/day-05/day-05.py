from mylib.aoc_basics import Day


class Computer:
    def __init__(self, program):
        self.program = program

    def execute_program(self, input_parameter):
        pc = 0
        program = list(self.program)
        while True:
            instruction = program[pc]
            opcode, modes = self.__decode_instruction(instruction)
            match opcode:
                case 1:
                    params = self.__get_parameters(program, pc + 1, 3, modes)
                    program[params[2]] = params[0] + params[1]
                    pc += 4
                case 2:
                    params = self.__get_parameters(program, pc + 1, 3, modes)
                    program[params[2]] = params[0] * params[1]
                    pc += 4
                case 3:
                    program[program[pc + 1]] = input_parameter
                    pc += 2
                case 4:
                    param = self.__get_parameters(program, pc + 1, 1, modes)[0]
                    output_parameter = param
                    pc += 2
                case 5:
                    params = self.__get_parameters(program, pc + 1, 2, modes)
                    if params[0] != 0:
                        pc = params[1]
                    else:
                        pc += 3
                case 6:
                    params = self.__get_parameters(program, pc + 1, 2, modes)
                    if params[0] == 0:
                        pc = params[1]
                    else:
                        pc += 3
                case 7:
                    params = self.__get_parameters(program, pc + 1, 3, modes)
                    program[params[2]] = 1 if params[0] < params[1] else 0
                    pc += 4
                case 8:
                    params = self.__get_parameters(program, pc + 1, 3, modes)
                    program[params[2]] = 1 if params[0] == params[1] else 0
                    pc += 4
                case 99:
                    break
                case _:
                    raise RuntimeError(f"Invalid opcode {opcode} at position {pc}")

        return output_parameter

    @staticmethod
    def __decode_instruction(instruction):
        opcode = instruction % 100
        mode1 = instruction // 100 % 10
        mode2 = instruction // 1000 % 10
        return opcode, [mode1, mode2, 1]

    @staticmethod
    def __get_parameters(program, start, count, modes):
        return [program[program[start + i]] if modes[i] == 0 else program[start + i] for i in range(count)]


class PartA(Day):
    def parse(self, text, data):
        data.program = [int(x) for x in text.split(",")]

    def compute(self, data):
        return Computer(data.program).execute_program(1)

    def example_answer(self):
        return 1

    def get_example_input(self, puzzle):
        return "3,0,4,0,99"


class PartB(PartA):
    def compute(self, data):
        return Computer(data.program).execute_program(5)

    def example_answer(self):
        return 999

    def get_example_input(self, puzzle):
        return "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"


Day.do_day(5, 2019, PartA, PartB)
