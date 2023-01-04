import math
import re
import itertools


def read_input_from_file(file_name):
    input_file = open(file_name, "r")
    input = input_file.readlines()
    input = [x.strip() for x in input]
    input_file.close()
    return input


def add(data):
    if " + " in data:
        left_number, right_number = data.split(" + ")
        data = f"[{left_number},{right_number}]"
    return data


def explode(data):
    offset = 0
    for number in re.findall(r"\[\d+,\d+]", data):
        pair = re.search(re.escape(number), data[offset:])
        num_left_brackets = data[:pair.start() + offset].count("[")
        num_right_brackets = data[:pair.start() + offset].count("]")
        if num_left_brackets - num_right_brackets >= 4:
            left, right = pair.group()[1:-1].split(",")
            left_part = data[:pair.start() + offset][::-1]
            right_part = data[pair.end() + offset:]
            search_left = re.search(r"\d+", left_part)
            if search_left:
                x = int(left_part[search_left.start():search_left.end()][::-1]) + int(left)
                left_part = f"{left_part[:search_left.start()]}{str(x)[::-1]}{left_part[search_left.end():]}"
            search_right = re.search(r"\d+", right_part)
            if search_right:
                x = int(right_part[search_right.start():search_right.end()]) + int(right)
                right_part = f"{right_part[:search_right.start()]}{str(x)}{right_part[search_right.end():]}"
            data = f"{left_part[::-1]}0{right_part}"
            break
        else:
            offset += pair.end()

    return data


def split(data):
    number = re.search(r"\d\d", data)
    if number:
        left_part = data[:number.start()]
        right_part = data[number.end():]
        new_left_digit = int(math.floor(int(number.group()) / 2))
        new_right_digit = int(math.ceil(int(number.group()) / 2))
        data = f"{left_part}[{new_left_digit},{new_right_digit}]{right_part}"
    return data


def reduce(data):
    exploded = explode(data)
    if exploded != data:
        return reduce(exploded)
    else:
        splitted = split(data)
        if splitted != data:
            return reduce(splitted)
    return splitted


def magnitude(data):
    while data.count(",") > 1:
        for number in re.findall(r"\[\d+,\d+\]", data):
            pair = re.search(re.escape(number), data)
            left_digit, right_digit = number[1:-1].split(",")
            data = f"{data[:pair.start()]}{int(left_digit) * 3 + int(right_digit) * 2}{data[pair.end():]}"
    left_digit, right_digit = data[1:-1].split(",")
    return int(left_digit) * 3 + int(right_digit) * 2


def part1(input):
    number = input[0]
    for line in input[1:]:
        number = f"{number} + {line}"
        number = add(number)
        number = reduce(number)
    print(f"Part 1 magnitude: {magnitude(number)}")


def part2(input):
    magnitudes = []
    pairs = list(itertools.permutations(input, 2))
    for pair in pairs:
        number = f"{pair[0]} + {pair[1]}"
        number = add(number)
        number = reduce(number)
        magnitudes.append(magnitude(number))
    print(f"Part2 max magnitude: {max(magnitudes)}")


def main():
    input = read_input_from_file("day-18/input.txt")

    part1(input)
    part2(input)


if __name__ == "__main__":
    main()
