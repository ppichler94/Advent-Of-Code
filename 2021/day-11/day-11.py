import numpy as np


def read_input_from_file(file_name):
    input_file = open(file_name, "r")
    input = input_file.readlines()
    input = [x.strip() for x in input]
    input_file.close()
    return input


def increase_around(energy_levels, position):
    i_min = max(0, position[0] - 1)
    i_max = min(energy_levels.shape[1], position[0] + 2)
    j_min = max(0, position[1] - 1)
    j_max = min(energy_levels.shape[0], position[1] + 2)
    energy_levels[i_min:i_max, j_min:j_max] += 1


def do_step(energy_levels):
    number_of_flashes = 0
    energy_levels += 1
    flashed = np.zeros(energy_levels.shape, dtype=bool)
    flashing = np.logical_and(energy_levels > 9, ~flashed)
    flashing = list(np.transpose(flashing.nonzero()))
    while len(flashing) > 0:
        index = flashing.pop()
        increase_around(energy_levels, index)
        flashed[index[0], index[1]] = True
        number_of_flashes += 1
        flashing = np.logical_and(energy_levels > 9, ~flashed)
        flashing = list(np.transpose(flashing.nonzero()))
    energy_levels[flashed] = 0
    return number_of_flashes


def day11a(input):
    number_of_flashes = 0
    energy_levels = np.array([list(line) for line in input], dtype=int)
    for _ in range(0, 100):
        number_of_flashes += do_step(energy_levels)
    return number_of_flashes


def day11b(input):
    energy_levels = np.array([list(line) for line in input], dtype=int)
    steps = 0
    while True:
        do_step(energy_levels)
        steps += 1
        if np.all(energy_levels == energy_levels[0]):
            return steps
    return steps


def main():
    example = read_input_from_file("day-11/example.txt")
    input = read_input_from_file("day-11/input.txt")

    print(f'Result example A: {day11a(example)}\n')
    print(f'Result puzzle data A: {day11a(input)}\n')
    print(f'Result example B: {day11b(example)}\n')
    print(f'Result puzzle data B: {day11b(input)}\n')


if __name__ == "__main__":
    main()
