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
    fully_contained_pairs = 0
    for line in input:
        start1, end1, start2, end2 = parse_line(line)
        if fully_contains(start1, end1, start2, end2):
            fully_contained_pairs += 1
    return fully_contained_pairs


def parse_line(line):
    sections = line.split(",")
    range1 = sections[0].split("-")
    range2 = sections[1].split("-")
    return int(range1[0]), int(range1[1]), int(range2[0]), int(range2[1])


def fully_contains(start1, end1, start2, end2):
    return (start1 <= start2 and end1 >= end2) or (start2 <= start1 and end2 >= end1)


def solve_b(input):
    overlapping_pairs = 0
    for line in input:
        start1, end1, start2, end2 = parse_line(line)
        if overlaps(start1, end1, start2, end2):
            overlapping_pairs += 1
    return overlapping_pairs


def overlaps(start1, end1, start2, end2):
    if start1 >= start2 and start1 <= end2:
        return True
    if end1 >= start2 and end1 <= end2:
        return True
    if start2 >= start1 and start2 <= end1:
        return True
    if end2 >= start1 and end2 <= end1:
        return True
    return False


if __name__ == "__main__":
    main()
