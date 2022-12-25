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
    data = [x.strip() for x in data]
    input_file.close()
    return data


def solve_a(input):
    calories_per_elf = calculate_calories_per_elf(input)
    return max(calories_per_elf)


def solve_b(input):
    calories_per_elf = calculate_calories_per_elf(input)
    calories_per_elf = sorted(calories_per_elf)
    return sum(calories_per_elf[-3:])


def calculate_calories_per_elf(input):
    calories_per_elf = []
    accumulator = 0
    for item in input:
        if not item:
            calories_per_elf.append(accumulator)
            accumulator = 0
        else:
            accumulator += int(item)
    calories_per_elf.append(accumulator)
    return calories_per_elf


if __name__ == "__main__":
    main()
