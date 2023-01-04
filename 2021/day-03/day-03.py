def readInputFromFile(fileName):
    inputFile = open(fileName, "r")
    input = inputFile.readlines()
    input = [x.strip() for x in input]
    inputFile.close()
    return input


def getMostCommonBitAtPos(input, index):
    numberOf0s = 0
    numberOf1s = 0
    for currentInput in input:
        if currentInput[index] == "0":
            numberOf0s += 1
        elif currentInput[index] == "1":
            numberOf1s += 1
    if numberOf1s >= numberOf0s:
        return 1
    else:
        return 0


def day03A(input):
    gammaRate = []
    epsilonRate = []
    for index in range(0, len(input[0])):
        result = getMostCommonBitAtPos(input, index)
        gammaRate.append(str(result))
        epsilonRate.append(str(1-result))
    gammaRate = "".join(gammaRate)
    epsilonRate = "".join(epsilonRate)
    gammaRate = int(gammaRate, 2)
    epsilonRate = int(epsilonRate, 2)
    print(f'gamma rate: {gammaRate} | epsilon rate: {epsilonRate}')
    return gammaRate * epsilonRate


def day03B(input):
    input2 = input.copy()

    for index in range(0, len(input[0])):
        bit = getMostCommonBitAtPos(input, index)
        i = 0
        while i < len(input):
            current = input[i]
            if current[index] != str(bit):
                input.pop(i)
            else:
                i += 1
        if (len(input) == 1):
            break

    for index in range(0, len(input2[0])):
        bit = getMostCommonBitAtPos(input2, index)
        i = 0
        while i < len(input2):
            current = input2[i]
            if current[index] != str(1-bit):
                input2.pop(i)
            else:
                i += 1
        if (len(input2) == 1):
            break

    oxygenRating = int(input[0], 2)
    scrubberRating = int(input2[0], 2)
    print(f'oxygen rating: {oxygenRating} | co2 scrubber rating: {scrubberRating}')

    return oxygenRating * scrubberRating


def main():
    example = readInputFromFile("day-03/example.txt")
    input = readInputFromFile("day-03/input.txt")

    print(f'Result example A: {day03A(example)}\n')
    print(f'Result puzzle data A: {day03A(input)}\n')
    print(f'Result example B: {day03B(example)}\n')
    print(f'Result puzzle data B: {day03B(input)}\n')


if __name__ == "__main__":
    main()
