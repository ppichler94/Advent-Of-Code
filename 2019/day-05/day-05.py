from mylib.aoc_basics import Day


class PartA(Day):
    def parse(self, text, data):
        data.program = [int(x) for x in text.split(",")]

    def compute(self, data):
        return self.execute_program(data.program, 1)

    def execute_program(self, program, input_parameter):
        pc = 0
        while True:
            instruction = program[pc]
            opcode, mode1, mode2 = self.decode_instruction(instruction)
            match opcode:
                case 1:
                    param1 = self.get_parameter(program, program[pc + 1], mode1)
                    param2 = self.get_parameter(program, program[pc + 2], mode2)
                    param3 = program[pc + 3]
                    program[param3] = param1 + param2
                    pc += 4
                case 2:
                    param1 = self.get_parameter(program, program[pc + 1], mode1)
                    param2 = self.get_parameter(program, program[pc + 2], mode2)
                    param3 = program[pc + 3]
                    program[param3] = param1 * param2
                    pc += 4
                case 3:
                    program[program[pc + 1]] = input_parameter
                    pc += 2
                case 4:
                    param = self.get_parameter(program, program[pc + 1], mode1)
                    output_parameter = param
                    pc += 2
                case 5:
                    param1 = self.get_parameter(program, program[pc + 1], mode1)
                    param2 = self.get_parameter(program, program[pc + 2], mode2)
                    if param1 != 0:
                        pc = param2
                    else:
                        pc += 3
                case 6:
                    param1 = self.get_parameter(program, program[pc + 1], mode1)
                    param2 = self.get_parameter(program, program[pc + 2], mode2)
                    if param1 == 0:
                        pc = param2
                    else:
                        pc += 3
                case 7:
                    param1 = self.get_parameter(program, program[pc + 1], mode1)
                    param2 = self.get_parameter(program, program[pc + 2], mode2)
                    param3 = program[pc + 3]
                    program[param3] = 1 if param1 < param2 else 0
                    pc += 4
                case 8:
                    param1 = self.get_parameter(program, program[pc + 1], mode1)
                    param2 = self.get_parameter(program, program[pc + 2], mode2)
                    param3 = program[pc + 3]
                    program[param3] = 1 if param1 == param2 else 0
                    pc += 4
                case 99:
                    break
                case _:
                    raise RuntimeError(f"Invalid opcode {opcode} at position {pc}")

        return output_parameter

    @staticmethod
    def decode_instruction(instruction):
        opcode = instruction % 100
        mode1 = instruction // 100 % 10
        mode2 = instruction // 1000 % 10
        return opcode, mode1, mode2

    @staticmethod
    def get_parameter(program, value, mode):
        if mode == 0:
            return program[value]
        else:
            return value

    def example_answer(self):
        return 1

    def get_example_input(self, puzzle):
        return "3,0,4,0,99"


class PartB(PartA):
    def compute(self, data):
        return self.execute_program(data.program, 5)

    def example_answer(self):
        return 999

    def get_example_input(self, puzzle):
        return "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"


Day.do_day(5, 2019, PartA, PartB)
