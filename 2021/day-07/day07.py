import numpy as np


def readInputFromFile(fileName):
    inputFile = open(fileName, "r")
    input = inputFile.readlines()
    input = [x.strip() for x in input]
    inputFile.close()
    return input


def costFunctionA(positions, target):
    return np.absolute(positions - target).sum()


def costFunctionB(positions, target):
    distance = np.absolute(positions - target)
    return (distance * (distance + 1) * 0.5).sum()


def calculateFuelUsage(positions, costFunction):
    min = positions.min()
    max = positions.max()
    minimalCost = costFunction(positions, min)
    minimalTarget = min
    for target in range(min, max):
        cost = costFunction(positions, target)
        if cost < minimalCost:
            minimalCost = cost
            minimalTarget = target

    return [minimalCost, minimalTarget]


def day07A(input):
    positions = np.array(input[0].split(","), dtype=int)

    [minimalCost, minimalTarget] = calculateFuelUsage(positions, costFunctionA)

    return minimalCost


def day07B(input):
    positions = np.array(input[0].split(","), dtype=int)

    [minimalCost, minimalTarget] = calculateFuelUsage(positions, costFunctionB)

    return minimalCost

def main():
    example = readInputFromFile("day-07/example.txt")
    input = readInputFromFile("day-07/input.txt")

    print(f'Result example A: {day07A(example)}\n')
    print(f'Result puzzle data A: {day07A(input)}\n')
    print(f'Result example B: {day07B(example)}\n')
    print(f'Result puzzle data B: {day07B(input)}\n')


if __name__ == "__main__":
    main()
