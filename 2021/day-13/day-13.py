import numpy as np


def read_input_from_file(file_name):
    input_file = open(file_name, "r")
    input = input_file.readlines()
    input = [x.strip() for x in input]
    input_file.close()
    return input


def parse_lines(input):
    points = []
    commands = []
    command_section = False
    for line in input:
        if line == "":
            command_section = True
            continue
        if not command_section:
            points.append([int(x) for x in line.split(",")])
        else:
            command = line.split(" ")[2].split("=")
            command[1] = int(command[1])
            commands.append(command)

    paper = build_paper(points)
    return [paper, commands]


def build_paper(points):
    x = max(point[0] for point in points) + 1
    y = max(point[1] for point in points) + 1

    paper = np.zeros((y, x))

    for point in points:
        paper[point[1], point[0]] = 1
    return paper


def do_folds(paper, commands):
    for command in commands:
        match command:
            case ["y", y]:
                upper = paper[0:y, :]
                lower = np.zeros(upper.shape)
                lower[-(paper.shape[0] - y - 1):, :] = np.flipud(paper[y + 1:paper.shape[0], :])
                paper = upper + lower
            case ["x", x]:
                left = paper[:, 0:x]
                right = np.zeros(left.shape)
                right[:, -(paper.shape[1] - x - 1):] = np.fliplr(paper[:, x + 1:paper.shape[1]])
                paper = left + right
    return paper


def day13a(input):
    [paper, commands] = parse_lines(input)
    paper = do_folds(paper, [commands[0]])
    return np.count_nonzero(paper)


def day13b(input):
    [paper, commands] = parse_lines(input)
    paper = do_folds(paper, commands)
    output = ""
    for row in paper:
        output += "\n" + "".join([" " if x == 0 else "#" for x in row])
    return output


def main():
    example = read_input_from_file("day-13/example.txt")
    input = read_input_from_file("day-13/input.txt")

    print(f'Result example A: {day13a(example)}\n')
    print(f'Result puzzle data A: {day13a(input)}\n')
    print(f'Result example B: {day13b(example)}\n')
    print(f'Result puzzle data B: {day13b(input)}\n')


if __name__ == "__main__":
    main()
