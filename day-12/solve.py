import numpy as np


def main():
    example_data = read_input_from_file("example.txt")
    input_data = read_input_from_file("input.txt")

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
    data, start, end = parse_input(input)
    distance = run_steps(data, start, end)
    return distance


def parse_input(input):
    data = np.empty([len(input[0]), len(input)], dtype=int)
    start = [0, 0]
    end = [0, 0]
    for y in range(len(input)):
        characters = [*input[y]]
        for x in range(len(characters)):
            match characters[x]:
                case 'S':
                    start = [x, y]
                    data[x,y] = 0
                case 'E':
                    end = [x, y]
                    data[x, y] = 25
                case c:
                    data[x, y] = (ord(c) - ord('a'))
    return data, start, end


def run_steps(data, start, end):

    def visit(x, y, distance):
        if distance + 1 < distance_map[x, y]:
            distance_map[x, y] = distance + 1
        possible_movements = get_possible_movements(data, x, y, distance + 1, distance_map)
        possible_movements = filter(lambda movement: movement not in to_visit, possible_movements)
        to_visit.extend(possible_movements)

    distance_map = np.full(data.shape, data.shape[0] * data.shape[1]+ 1, dtype=int)
    distance_map[start[0], start[1]] = 0
    to_visit = [[0, 0, -1]]
    while len(to_visit) > 0:
        [new_x, new_y, previous_distance] = to_visit.pop(0)
        visit(new_x, new_y, previous_distance)

    return distance_map[end[0], end[1]]


def get_possible_movements(data, x, y, distance, distance_map):
    movements = []
    if x > 0 and data[x - 1, y] <= data[x, y] + 1 and distance <= distance_map[x - 1, y]:
        movements.append([x - 1, y, distance])
    if x < data.shape[0] - 1 and data[x + 1, y] <= data[x, y] + 1 and distance <= distance_map[x + 1, y]:
        movements.append([x + 1, y, distance])
    if y > 0 and data[x, y - 1] <= data[x, y] + 1 and distance <= distance_map[x, y - 1]:
        movements.append([x, y - 1, distance])
    if y < data.shape[1] - 1 and data[x, y + 1] <= data[x, y] + 1 and distance <= distance_map[x, y + 1]:
        movements.append([x, y + 1, distance])
    return movements


def solve_b(input):
    return


if __name__ == "__main__":
    main()
