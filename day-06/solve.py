def main():
    example_data = read_input_from_file("example.txt")
    input_data = read_input_from_file("input.txt")

    print(f'Result example A: {solve(example_data, 4)}\n')
    print(f'Result puzzle data A: {solve(input_data, 4)}\n')
    print(f'Result example B: {solve(example_data, 14)}\n')
    print(f'Result puzzle data B: {solve(input_data, 14)}\n')


def read_input_from_file(file_name):
    input_file = open(file_name, "r")
    data = input_file.readlines()
    input_file.close()
    data = [x.strip() for x in data]
    return data[0]


def solve(input, packet_length):
    for i in range(packet_length, len(input)):
        if all_different(input[i-packet_length:i]):
            return i


def all_different(text):
    set_text = set(text)
    return len(set_text) == len(text)


if __name__ == "__main__":
    main()
