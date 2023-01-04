import numpy as np


def readInputFromFile(fileName):
    inputFile = open(fileName, "r")
    input = inputFile.readlines()
    input = [x.strip() for x in input]
    inputFile.close()
    return input


class Population:

    def __init__(self, input) -> None:
        population = np.array([int(x) for x in input[0].split(",")])
        self.bins = np.zeros(10)
        for i in range(0, 10):
            self.bins[i] = (population == i).sum()

    def __tick(self):
        self.bins = np.roll(self.bins, -1)

    def __spawnNew(self):
        numberOfZeros = self.bins[0]
        self.bins[0] = 0
        self.bins[7] += numberOfZeros
        self.bins[9] += numberOfZeros

    def simulateDays(self, numberOfDays):
        for day in range(0, numberOfDays):
            self.__spawnNew()
            self.__tick()

    def size(self):
        return self.bins.sum()


def day06A(input):
    population = Population(input)
    population.simulateDays(80)
    return population.size()


def day06B(input):
    population = Population(input)
    population.simulateDays(256)
    return population.size()


def main():
    example = readInputFromFile("day-06/example.txt")
    input = readInputFromFile("day-06/input.txt")

    print(f'Result example A: {day06A(example)}\n')
    print(f'Result puzzle data A: {day06A(input)}\n')
    print(f'Result example B: {day06B(example)}\n')
    print(f'Result puzzle data B: {day06B(input)}\n')


if __name__ == "__main__":
    main()
