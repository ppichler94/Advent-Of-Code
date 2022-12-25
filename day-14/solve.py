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
    cave, max_y = parse_input(input)
    sand_resting = True
    while sand_resting:
        sand_resting = add_sand(cave, max_y)
    return np.count_nonzero(cave == 2)


def parse_input(input):
    cave = np.zeros([500, 1000], dtype=int)
    for line in input:
        parts = line.split(" -> ")
        for i in range(len(parts) - 1):
            x1 = int(parts[i].split(",")[0])
            y1 = int(parts[i].split(",")[1])
            x2 = int(parts[i+1].split(",")[0])
            y2 = int(parts[i+1].split(",")[1])

            x_start = min(x1, x2)
            x_end = max(x1, x2) + 1
            y_start = min(y1, y2)
            y_end = max(y1, y2) + 1

            cave[y_start:y_end,x_start:x_end] = 1
    max_y = np.max(np.argwhere(cave == 1), axis=0)[0]
    return cave, max_y


def add_sand(cave, max_y):
    x = 500
    y = 0
    while 1:
        if y > max_y:
            return False
        if cave[y + 1, x] == 0:
            y += 1
        elif cave[y + 1, x - 1] == 0:
            y += 1
            x -= 1
        elif cave[y + 1, x + 1] == 0:
            y += 1
            x += 1
        else:
            cave[y, x] = 2
            return True



def solve_b(input):
    return


if __name__ == "__main__":
    main()
