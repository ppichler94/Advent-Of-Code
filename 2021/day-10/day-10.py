import numpy as np


def read_input_from_file(file_name):
    input_file = open(file_name, "r")
    input = input_file.readlines()
    input = [x.strip() for x in input]
    input_file.close()
    return input


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


def get_points_for_corrupt_line(line):
    point_table = {")": 3, "]": 57, "}": 1197, ">": 25137}
    stack = []
    for character in line:
        matching = check_character(character, stack)
        if not matching:
            return point_table[character]
    return 0


def get_points_to_finish_line(line):
    point_table = {"(": 1, "[": 2, "{": 3, "<": 4}
    stack = []
    for character in line:
        check_character(character, stack)
    points = 0
    stack.reverse()
    for c in stack:
        points = points * 5 + point_table[c]
    return points


def day10a(input):
    points = 0
    for line in input:
        points += get_points_for_corrupt_line(line)
    return points


def day10b(input):
    points = []
    index = 0
    while index < len(input):
        line = input[index]
        corrupt = get_points_for_corrupt_line(line) > 0
        if corrupt:
            input.pop(index)
        else:
            index += 1
    for line in input:
        points.append(get_points_to_finish_line(line))
    points = np.array(points)

    return np.median(points)


def main():
    example = read_input_from_file("day-10/example.txt")
    input = read_input_from_file("day-10/input.txt")

    print(f'Result example A: {day10a(example)}\n')
    print(f'Result puzzle data A: {day10a(input)}\n')
    print(f'Result example B: {day10b(example)}\n')
    print(f'Result puzzle data B: {day10b(input)}\n')


if __name__ == "__main__":
    main()
