def readInputFromFile(fileName):
    inputFile = open(fileName, "r")
    input = inputFile.readlines()
    input = [x.strip() for x in input]
    inputFile.close()
    return input


def day01A(input):
    increase = 0
    previous = int(input.pop(0))
    for current in input:
        value = int(current)
        if (value > previous):
            increase += 1
        previous = value

    return increase


def day01B(input):
    depthOfWindow = []
    for i in range(0, len(input)-2):
        sum = 0
        for j in range(0, 3):
            sum += int(input[i+j])
        depthOfWindow.append(sum)

    increase = 0
    previous = depthOfWindow.pop(0)
    for value in depthOfWindow:
        if (value > previous):
            increase += 1
        previous = value

    return increase


def main():
    example = readInputFromFile("day-01/example.txt")
    input = readInputFromFile("day-01/input.txt")

    print(f'Result example A: {day01A(example)}\n')
    print(f'Result puzzle data A: {day01A(input)}\n')
    print(f'Result example B: {day01B(example)}\n')
    print(f'Result puzzle data B: {day01B(input)}\n')


if __name__ == "__main__":
    main()
