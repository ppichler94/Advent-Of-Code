import numpy as np

def main():
    example_data = read_input_from_file("day-08/example.txt")
    input_data = read_input_from_file("day-08/input.txt")

    print(f'Result example A: {solve_a(example_data)}\n')
    print(f'Result puzzle data A: {solve_a(input_data)}\n')
    print(f'Result example B: {solve_b(example_data)}\n')
    print(f'Result puzzle data B: {solve_b(input_data)}\n')


def read_input_from_file(file_name):
    input_file = open(file_name, "r")
    data = input_file.readlines()
    input_file.close()
    data = [x.strip() for x in data]
    data = np.array([list(line) for line in data], dtype=int)
    return data


def solve_a(input):
    visibility = calculate_visibility(input)
    return np.count_nonzero(visibility)


def calculate_visibility(input):
    visibility = np.zeros(input.shape, dtype=bool)
    calculate_visibility_row(input, visibility, 0, input.shape[1], 1)
    calculate_visibility_row(input, visibility, input.shape[1] - 1, -1, -1)
    calculate_visibility_col(input, visibility, 0, input.shape[0], 1)
    calculate_visibility_col(input, visibility, input.shape[0] - 1, -1, -1)
    return visibility


def calculate_visibility_row(input, visibility, start, stop, step):
    for row in range(0, input.shape[0]):
        current_height = -1
        for col in range(start, stop, step):
            if input[row, col] > current_height:
                visibility[row, col] |= True
                current_height = input[row, col]


def calculate_visibility_col(input, visibility, start, stop, step):
    for col in range(0, input.shape[1]):
        current_height = -1
        for row in range(start, stop, step):
            if input[row, col] > current_height:
                visibility[row, col] |= True
                current_height = input[row, col]


def solve_b(input):
    scenic_score = calculate_scenic_scores(input)
    return np.max(scenic_score)


def calculate_scenic_scores(input):
    score = np.zeros(input.shape, dtype=int)
    return score


if __name__ == "__main__":
    main()
