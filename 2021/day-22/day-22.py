import os
import parse
from collections import namedtuple
import numpy as np
from typing import List

Step = namedtuple("Step", "activate x_min x_max y_min y_max z_min z_max")


def read_input_from_file(file_name: str) -> list:
    script_path = os.path.dirname(os.path.abspath(__file__))
    input_file = open(f"{script_path}/{file_name}", "r")
    data = input_file.readlines()
    data = [x.strip() for x in data]
    input_file.close()
    return data


def execute_step(grid: np.ndarray, step) -> None:
    x_min = max(0, step.x_min + 50)
    x_max = min(101, step.x_max + 51)
    y_min = max(0, step.y_min + 50)
    y_max = min(101, step.y_max + 51)
    z_min = max(0, step.z_min + 50)
    z_max = min(101, step.z_max + 51)
    grid[x_min:x_max, y_min:y_max, z_min:z_max] = step.activate


def execute_steps(grid: np.ndarray, steps: List[Step]):
    for step in steps:
        execute_step(grid, step)


def parse_input(data):
    steps = []
    for line in data:
        result = parse.parse("{:w} x={:d}..{:d},y={:d}..{:d},z={:d}..{:d}", line)
        steps.append(Step(result[0] == "on", result[1], result[2], result[3], result[4], result[5], result[6]))
    return steps


def part_a(data):
    grid = np.zeros((101, 101, 101), dtype=bool)
    steps = parse_input(data)

    execute_steps(grid, steps)
    print(f"Part 1 active cubes: {np.count_nonzero(grid)}")


def intersect(a: Step, b: Step) -> Step:
    isec = Step(not b.activate, max(a.x_min, b.x_min), min(a.x_max, b.x_max), max(a.y_min, b.y_min), min(a.y_max, b.y_max), max(a.z_min, b.z_min), min(a.z_max, b.z_max))
    if isec.x_min > isec.x_max or isec.y_min > isec.y_max or isec.z_min > isec.z_max:
        return None
    return isec


def count_cubes(reactor: List[Step]):
    count = 0
    for core in reactor:
        prefix = 1 if core.activate else -1
        count += prefix * (core.x_max - core.x_min + 1) * (core.y_max - core.y_min + 1) * (core.z_max - core.z_min + 1)
    return count


def part_b(data):
    reactor = []
    steps = parse_input(data)

    for step in steps:
        add_list = []
        if step.activate:
            add_list.append(step)
        for core in reactor:
            isec = intersect(step, core)
            if isec:
                add_list.append(isec)
        reactor += add_list

    count = count_cubes(reactor)
    print(f"Part 2 active cubes: {count}")


def main() -> None:
    example_data = read_input_from_file("example.txt")
    data = read_input_from_file("input.txt")

    part_a(data)
    part_b(data)


if __name__ == "__main__":
    main()
