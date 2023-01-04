import numpy as np
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder


def read_input_from_file(file_name):
    input_file = open(file_name, "r")
    input = input_file.readlines()
    input = [x.strip() for x in input]
    input_file.close()
    return input


def create_map_a(input):
    return np.array([[int(x) for x in list(line)] for line in input])


def create_map_b(input):
    map_part = np.array([[int(x) for x in list(line)] for line in input])
    cave_map = np.empty(0)
    for i in range(0, 5):
        part = map_part + i
        part[part > 9] -= 9
        line_map = np.array(part)
        for j in range(1, 5):
            part = map_part + i + j
            part[part > 9] -= 9
            line_map = np.concatenate((line_map, part), axis=1)
        if i == 0:
            cave_map = line_map
        else:
            cave_map = np.concatenate((cave_map, line_map), axis=0)

    return cave_map


def run(input, create_map_function):
    cave_map = create_map_function(input)
    grid = Grid(matrix=cave_map)
    start = grid.node(0, 0)
    end = grid.node(len(cave_map) - 1, len(cave_map) - 1)

    finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
    path, _ = finder.find_path(start, end, grid)
    risk = sum(cave_map[x[1]][x[0]] for x in path[1:])
    return risk


def main():
    example = read_input_from_file("day-15/example.txt")
    input = read_input_from_file("day-15/input.txt")

    print(f'Result example A: {run(example, create_map_a)}\n')
    print(f'Result puzzle data A: {run(input, create_map_a)}\n')
    print(f'Result example B: {run(example, create_map_b)}\n')
    print(f'Result puzzle data B: {run(input, create_map_b)}\n')


if __name__ == "__main__":
    main()
