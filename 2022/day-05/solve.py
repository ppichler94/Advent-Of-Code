from collections import namedtuple
import re
from mylib.aoc_basics import Day


Command = namedtuple("Command", ["origin", "destination", "count"])


class PartA(Day):
    def parse(self, text, data):
        stack_text, move_text = text.split("\n\n")
        stack_lines = stack_text.splitlines()
        data.stacks = ["" for _ in range(len(re.findall(r"\d+", stack_lines[-1])))]
        for line in stack_lines:
            for i in range(len(line)):
                if ord("A") <= ord(line[i]) <= ord("Z"):
                    pos = int((i - 1) / 4)
                    data.stacks[pos] += line[i]
        data.stacks = [stack[::-1] for stack in data.stacks]

        data.commands = []
        for line in move_text.splitlines():
            matcher = re.search(r"move (\d*) from (\d*) to (\d*)", line)
            if matcher:
                data.commands.append(Command(int(matcher.group(2)) - 1, int(matcher.group(3)) - 1, int(matcher.group(1))))

    def compute(self, data):
        self.crate_mover(data.stacks, data.commands)
        return ''.join([stack[-1] for stack in data.stacks])

    def crate_mover(self, stacks, commands):
        for command in commands:
            for _ in range(command.count):
                stacks[command.destination] += stacks[command.origin][-1]
                stacks[command.origin] = stacks[command.origin][:-1]

    def example_answer(self):
        return "CMZ"


class PartB(PartA):
    def crate_mover(self, stacks, commands):
        for command in commands:
            stacks[command.destination] += stacks[command.origin][-command.count:]
            stacks[command.origin] = stacks[command.origin][:-command.count]

    def example_answer(self):
        return "MCD"


Day.do_day(5, 2022, PartA, PartB)
