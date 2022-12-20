import numpy as np


def main():
    example_data = read_input_from_file("day-09/example.txt")
    input_data = read_input_from_file("day-09/input.txt")

    print(f'Result example A: {solve_a(example_data)}\n')
    print(f'Result puzzle data A: {solve_a(input_data)}\n')
    print(f'Result example B: {solve_b(example_data)}\n')
    print(f'Result puzzle data B: {solve_b(input_data)}\n')


def read_input_from_file(file_name):
    input_file = open(file_name, "r")
    data = input_file.readlines()
    input_file.close()
    data = [x.strip() for x in data]
    return data


def solve_a(input):
    visited = set()
    head_pos = np.zeros(2, dtype=int)
    tail_pos = np.zeros(2, dtype=int)
    for line in input:
        execute_motion(line, visited, head_pos, tail_pos)
    return len(visited)


def execute_motion(motion, visited, head_pos, tail_pos):
    motion_parts = motion.split(" ")
    direction = motion_parts[0]
    count = int(motion_parts[1])
    for i in range(count):
        execute_step(direction, visited, head_pos, tail_pos)


def execute_step(direction, visited, head_pos, tail_pos):
    match direction:
        case "U":
            head_pos[1] += 1
        case "D":
            head_pos[1] -= 1
        case "R":
            head_pos[0] += 1
        case "L":
            head_pos[0] -= 1
    update_tail_pos(head_pos, tail_pos)
    visited.add(f'{tail_pos[0]}.{tail_pos[1]}')


def update_tail_pos(head_pos, tail_pos):
    diff = head_pos - tail_pos
    if np.linalg.norm(diff) < 2:
        return False
    if np.linalg.norm(diff) == 2:
        diff = diff / np.linalg.norm(diff)
    if np.linalg.norm(diff) > 2:
        diff = np.divide(diff, np.absolute(diff))
    tail_pos += np.rint(diff).astype(int)
    return True


def solve_b(input):
    visited = set()
    head_pos = np.zeros(2, dtype=int)
    knots = [np.zeros(2, dtype=int) for i in range(9)]
    for line in input:
        execute_motion_b(line, visited, head_pos, knots)
    return len(visited)


def execute_motion_b(motion, visited, head_pos, knots):
    motion_parts = motion.split(" ")
    direction = motion_parts[0]
    count = int(motion_parts[1])
    for i in range(count):
        execute_step_b(direction, visited, head_pos, knots)


def execute_step_b(direction, visited, head_pos, knots):
    match direction:
        case "U":
            head_pos[1] += 1
        case "D":
            head_pos[1] -= 1
        case "R":
            head_pos[0] += 1
        case "L":
            head_pos[0] -= 1
    update_tail_pos(head_pos, knots[0])
    for i in range(1, len(knots)):
        changed = update_tail_pos(knots[i - 1], knots[i])
        if not changed:
            break
    visited.add(f'{knots[-1][0]}.{knots[-1][1]}')


if __name__ == "__main__":
    main()
