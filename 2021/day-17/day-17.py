import math
import parse
import enum
import itertools


class Result(enum.Enum):
    Hit = 0
    Miss = 1


def read_input_from_file(file_name):
    input_file = open(file_name, "r")
    input = input_file.readlines()
    input = [x.strip() for x in input]
    input_file.close()
    return input


def sign(x):
    if x < 0:
        return -1
    if x > 0:
        return 1
    return 0


def calculate_trajectory(velocity, target):
    vx, vy = velocity
    x, y = 0, 0
    x_min, x_max, y_min, y_max = target

    while True:
        x += vx
        y += vy

        vx -= sign(vx)
        vy -= 1

        if x > x_max:
            return Result.Miss
        if y < y_min:
            return Result.Miss
        if x >= x_min and y <= y_max:
            return Result.Hit


def parse_target(input):
    result = parse.parse("target area: x={:d}..{:d}, y={:d}..{:d}", input)
    return list(result.fixed)


def part_b(input, title):
    print(title)
    target = parse_target(input[0])

    min_vy = target[2]
    max_vy = int(-target[2] - 1)
    min_vx = int(.5 * math.sqrt(1 + 8 * target[0]))
    max_vx = int(target[1])
    print(f"velocity range x={min_vx}..{max_vx} y={min_vy}..{max_vy}")
    velocities = list(itertools.product(range(min_vx, max_vx + 1), range(min_vy, max_vy + 1)))
    hits = []
    for velocity in velocities:
        result = calculate_trajectory(velocity, target)
        if result == Result.Hit:
            hits.append(velocity)

    print(f"found {len(hits)} initial velocities")


def part_a(input, title):
    print(title)
    target = parse_target(input[0])
    max_vy = int(-target[2] - 1)
    max_y = int(max_vy * (max_vy + 1) / 2)
    print(f"max y: {max_y}")


def main():
    example = read_input_from_file("day-17/example.txt")
    input = read_input_from_file("day-17/input.txt")

    part_a(example, f"example: {example[0]}")
    part_a(input, f"puzzle data: {input[0]}")

    part_b(example, f"example: {example[0]}")
    part_b(input, f"puzzle data: {input[0]}")


if __name__ == "__main__":
    main()
