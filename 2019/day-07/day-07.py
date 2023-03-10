from itertools import permutations
from mylib.aoc_basics import Day


class Computer:
    def __init__(self, program, input_parameters):
        self.program = list(program)
        self.pc = 0
        self.output = 0
        self.inputs = input_parameters

    def execute_program(self):
        while True:
            instruction = self.program[self.pc]
            opcode, modes = self.__decode_instruction(instruction)
            match opcode:
                case 1:
                    params = self.__get_parameters(self.program, self.pc + 1, 3, modes)
                    self.program[params[2]] = params[0] + params[1]
                    self.pc += 4
                case 2:
                    params = self.__get_parameters(self.program, self.pc + 1, 3, modes)
                    self.program[params[2]] = params[0] * params[1]
                    self.pc += 4
                case 3:
                    if not self.inputs:
                        return False
                    self.program[self.program[self.pc + 1]] = self.inputs.pop(0)
                    self.pc += 2
                case 4:
                    param = self.__get_parameters(self.program, self.pc + 1, 1, modes)[0]
                    self.output = param
                    self.pc += 2
                case 5:
                    params = self.__get_parameters(self.program, self.pc + 1, 2, modes)
                    if params[0] != 0:
                        self.pc = params[1]
                    else:
                        self.pc += 3
                case 6:
                    params = self.__get_parameters(self.program, self.pc + 1, 2, modes)
                    if params[0] == 0:
                        self.pc = params[1]
                    else:
                        self.pc += 3
                case 7:
                    params = self.__get_parameters(self.program, self.pc + 1, 3, modes)
                    self.program[params[2]] = 1 if params[0] < params[1] else 0
                    self.pc += 4
                case 8:
                    params = self.__get_parameters(self.program, self.pc + 1, 3, modes)
                    self.program[params[2]] = 1 if params[0] == params[1] else 0
                    self.pc += 4
                case 99:
                    return True
                case _:
                    raise RuntimeError(f"Invalid opcode {opcode} at position {self.pc}")

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
        all_phase_settings = permutations(range(5))
        max_output = 0
        for phase_settings in all_phase_settings:
            output = 0
            for i in range(5):
                computer = Computer(data.program, [phase_settings[i], output])
                computer.execute_program()
                output = computer.output
            max_output = max(output, max_output)
        return max_output

    def get_example_input(self, puzzle):
        return None

    def tests(self):
        yield "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0", 43210, "Example1"
        yield "3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0", 54321, "Example2"
        yield "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0", 65210, "Example3"


class PartB(PartA):
    def compute(self, data):
        all_phase_settings = permutations(range(5, 10))
        max_output = 0
        for phase_settings in all_phase_settings:
            computers = [Computer(data.program, [phase_settings[i]]) for i in range(5)]
            output = 0
            while True:
                for i in range(5):
                    computers[i].inputs.append(output)
                    halted = computers[i].execute_program()
                    output = computers[i].output
                if halted:
                    break
            max_output = max(output, max_output)
        return max_output

    def tests(self):
        yield "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5", 139629729, "Example1"
        yield "3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10", 18216, "Example2"


Day.do_day(7, 2019, PartA, PartB)
