from collections import namedtuple
import re


def main():
    example_data = read_input_from_file("example.txt")
    input_data = read_input_from_file("input.txt")

    print(f'Result example A: {solve(example_data, crate_mover_9000)}\n')
    print(f'Result puzzle data A: {solve(input_data, crate_mover_9000)}\n')
    print(f'Result example B: {solve(example_data, crate_mover_9001)}\n')
    print(f'Result puzzle data B: {solve(input_data, crate_mover_9001)}\n')


Command = namedtuple("Command", ["origin", "destination", "count"])


def read_input_from_file(file_name):
    input_file = open(file_name, "r")
    data = input_file.readlines()
    input_file.close()
    return data


def solve(input, crate_mover):
    stacks = parse_stacks(input)
    commands = parse_commands(input)
    crate_mover(stacks, commands)
    return ''.join([stack[-1] for stack in stacks])


def parse_stacks(input):
    stacks = ["" for _ in range(int(len(input[0]) / 4))]
    for line in input:
        for i in range(len(line)):
            if ord(line[i]) >= ord("A") and ord(line[i]) <= ord("Z"):
                pos = int((i - 1) / 4)
                stacks[pos] += line[i]
    stacks = [str[::-1] for str in stacks]
    return stacks


def parse_commands(input):
    commands = []
    for line in input:
        matcher = re.search(r"move (\d*) from (\d*) to (\d*)", line)
        if (matcher):
            commands.append(Command(int(matcher.group(2)) - 1, int(matcher.group(3)) - 1, int(matcher.group(1))))
    return commands


def crate_mover_9000(stacks, commands):
    for command in commands:
        for _ in range(command.count):
            stacks[command.destination] += stacks[command.origin][-1]
            stacks[command.origin] = stacks[command.origin][:-1]


def crate_mover_9001(stacks, commands):
    for command in commands:
        stacks[command.destination] += stacks[command.origin][-command.count:]
        stacks[command.origin] = stacks[command.origin][:-command.count]


if __name__ == "__main__":
    main()
