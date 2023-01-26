from mylib.aoc_basics import Day


class PartA(Day):
    def parse(self, text, data):
        data.instructions = [(op, int(arg)) for op, arg in [line.split(" ") for line in text.splitlines()]]

    def compute(self, data):
        acc, _ = self.run(data.instructions)
        return acc

    @staticmethod
    def run(instructions):
        acc = 0
        pc = 0
        executed = set()
        while True:
            if pc >= len(instructions):
                return acc, False
            executed.add(pc)
            op, arg = instructions[pc]
            match op:
                case "jmp":
                    pc += arg
                case "acc":
                    acc += arg
                    pc += 1
                case "nop":
                    pc += 1
            if pc in executed:
                return acc, True

    def example_answer(self):
        return 5


class PartB(PartA):
    def compute(self, data):
        change_dict = {"jmp": "nop", "nop": "jmp"}
        for current_trial in range(len(data.instructions)):
            instructions = list(data.instructions)
            if instructions[current_trial][0] not in change_dict.keys():
                continue
            instructions[current_trial] = (change_dict[instructions[current_trial][0]], instructions[current_trial][1])
            acc, loop = self.run(instructions)
            if not loop:
                return acc

    def example_answer(self):
        return 8


Day.do_day(8, 2020, PartA, PartB)
