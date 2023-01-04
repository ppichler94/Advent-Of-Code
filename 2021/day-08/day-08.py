def read_input_from_file(file_name):
    input_file = open(file_name, "r")
    input = input_file.readlines()
    input = [x.strip() for x in input]
    input_file.close()
    return input


def day08a(input):
    unique_numbers = 0
    for line in input:
        output_value = line.split("|")[1]
        for value in output_value.split(" "):
            if len(value) in [2, 3, 4, 7]:
                unique_numbers += 1
    return unique_numbers


def format_input(input):
    return list(map(lambda w: ''.join(sorted(w)), input))


def find_uniques(line, tmp):
    length_map = {2: "1", 3: "7", 4: "4", 7: "8"}
    for word in line:
        if len(word) in length_map:
            tmp[length_map[len(word)]] = word


# one character is different between 1 and 6
def find6(line, tmp):
    for word in line:
        if len(word) == 6 and any(character not in word for character in tmp["1"]):
            tmp["6"] = word
            break


# one character is different between 0 and 4. Also one character difference to 6 (so find 6 first)
def find0(line, tmp):
    for word in line:
        if (len(word) == 6
                and any(character not in word for character in tmp["4"])
                and word not in tmp.values()):
            tmp["0"] = word
            break


# only 6 character number left after finding 0 and 6
def find9(line, tmp):
    for word in line:
        if len(word) == 6 and word not in tmp.values():
            tmp["9"] = word
            break


# all characters of 5 are in 6
def find5(line, tmp):
    for word in line:
        if len(word) == 5 and all(character in tmp["6"] for character in word):
            tmp["5"] = word
            break


# all characters of 3 are in 9 and 5 (find 5 first)
def find3(line, tmp):
    for word in line:
        if (len(word) == 5
                and all(character in tmp["9"] for character in word)
                and word not in tmp.values()):
            tmp["3"] = word
            break


# only 5 character number left after finding 5 and 3
def find2(line, tmp):
    for word in line:
        if len(word) == 5 and word not in tmp.values():
            tmp["2"] = word
            break


def day08b(input):
    pattern = list(map(format_input, [line.split("|")[0].strip().split() for line in input]))
    output = list(map(format_input, [line.split("|")[1].strip().split() for line in input]))
    total = 0

    for line, output_value in zip(pattern, output):
        tmp = {}

        find_uniques(line, tmp)
        find6(line, tmp)
        find0(line, tmp)
        find9(line, tmp)
        find5(line, tmp)
        find3(line, tmp)
        find2(line, tmp)

        code = {v: k for k, v in tmp.items()}

        total += int(''.join([code[word] for word in output_value]))

    return total


def main():
    example = read_input_from_file("day-08/example.txt")
    input = read_input_from_file("day-08/input.txt")

    print(f'Result example A: {day08a(example)}\n')
    print(f'Result puzzle data A: {day08a(input)}\n')
    print(f'Result example B: {day08b(example)}\n')
    print(f'Result puzzle data B: {day08b(input)}\n')


if __name__ == "__main__":
    main()
