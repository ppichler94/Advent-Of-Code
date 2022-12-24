from numpy import sign

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
    packet_pairs = parse_input(input)
    result = 0
    for index, [packet1, packet2] in enumerate(packet_pairs):
        print(f"\n== Pair {index+1} ==")
        comparison_result = compare_lists(packet1, packet2, 0)
        if comparison_result == -1:
            result += (index + 1)
            print(f"Pair is in right order")
    return result


def parse_input(input):
    pairs = []
    for i in range(0, len(input), 3):
        packet1 = eval(input[i])
        packet2 = eval(input[i + 1])
        pairs.append([packet1, packet2])
    return pairs


def compare_lists(list1, list2, offset):
    print(f'{" "*offset}Compare {list1} vs {list2}')
    while 1:
        if len(list1) == 0 and len(list2) == 0:
            return 0
        if len(list1) == 0:
            print(f'{" "*(offset+2)} Left side ran out of items')
            return -1
        if len(list2) == 0:
            print(f'{" "*(offset+2)} Right side ran out of items')
            return 1
        data1 = list1.pop(0)
        data2 = list2.pop(0)
        result = compare(data1, data2, offset + 2)
        if result != 0:
            return result


def compare(data1, data2, offset):
    print(f'{" "*offset}Compare {data1} vs {data2}')
    if type(data1) == list and type(data2) == list:
        return compare_lists(data1, data2, offset + 2)
    if type(data1) == int and type(data2) == int:
        if sign(data1 - data2) != 0:
            side = "Left" if sign(data1 - data2) < 0 else "Right"
            print(f'{" "*(offset+2)} {side} side is smaller')
        return sign(data1 - data2)
    if type(data1) != list:
        data1 = [data1]
    if type(data2) != list:
        data2 = [data2]
    return compare_lists(data1, data2, offset + 2)


def solve_b(input):
    return


if __name__ == "__main__":
    main()
