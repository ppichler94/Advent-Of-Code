def readInputFromFile(fileName):
    inputFile = open(fileName, "r")
    input = inputFile.readlines()
    input = [x.strip() for x in input]
    inputFile.close()
    return input


def day02A(input):
    horizontalPos = 0
    depth = 0

    for commandString in input:
        commands = commandString.split(" ")
        direction = commands[0]
        count = int(commands[1])

        if direction == "forward":
            horizontalPos += count
        elif direction == "down":
            depth += count
        elif direction == "up":
            depth -= count

    print(f'horizontal position: {horizontalPos} | depth: {depth}')
    return horizontalPos * depth


def day02B(input):
    horizontalPos = 0
    depth = 0
    aim = 0

    for commandString in input:
        commands = commandString.split(" ")
        direction = commands[0]
        count = int(commands[1])

        if direction == "forward":
            horizontalPos += count
            depth += aim * count
        elif direction == "down":
            aim += count
        elif direction == "up":
            aim -= count

    print(f'horizontal position: {horizontalPos} | depth: {depth}')
    return horizontalPos * depth


def main():
    example = readInputFromFile("day-02/example.txt")
    input = readInputFromFile("day-02/input.txt")

    print(f'Result example A: {day02A(example)}\n')
    print(f'Result puzzle data A: {day02A(input)}\n')
    print(f'Result example B: {day02B(example)}\n')
    print(f'Result puzzle data B: {day02B(input)}\n')


if __name__ == "__main__":
    main()
