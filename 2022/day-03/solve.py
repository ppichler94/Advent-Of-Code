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
    priority_sum = 0
    for line in input:
        size = len(line)
        compartment_size = int(size / 2)
        list_a = line[:compartment_size]
        list_b = line[compartment_size:]
        common_item = find_common_item(list_a, list_b)
        priority_sum += priority_of(common_item)
    return priority_sum


def solve_b(input):
    priority_sum = 0
    for i in range(0, len(input), 3):
        badge = find_common_item(*input[i:i+3])
        priority_sum += priority_of(badge)
    return priority_sum


def find_common_item(*lists):
    return set.intersection(*map(set, lists)).pop()


def priority_of(item):
    if (ord(item) >= ord('a') and ord(item) <= ord('z')):
        return 1 + ord(item) - ord('a')
    elif (ord(item) >= ord('A') and ord(item) <= ord('Z')):
        return 27 + ord(item) - ord('A')


if __name__ == "__main__":
    main()
