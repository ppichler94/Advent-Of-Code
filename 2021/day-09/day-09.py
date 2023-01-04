import numpy as np


def readInputFromFile(fileName):
    inputFile = open(fileName, "r")
    input = inputFile.readlines()
    input = [x.strip() for x in input]
    inputFile.close()
    return input


def getSurroundingValues(heatmap, i, j):
    left = heatmap[i, j - 1] if j > 0 else 9
    right = heatmap[i, j + 1] if j < heatmap.shape[1] - 1 else 9
    up = heatmap[i - 1, j] if i > 0 else 9
    down = heatmap[i + 1, j] if i < heatmap.shape[0] - 1 else 9
    return [left, right, up, down]


def getMinima(heatmap):
    minima = []
    for i in range(0, heatmap.shape[0]):
        for j in range(0, heatmap.shape[1]):
            value = heatmap[i, j]
            [left, right, up, down] = getSurroundingValues(heatmap, i, j)
            if value < left \
                    and value < right \
                    and value < up \
                    and value < down:
                minima.append([i, j])
    return minima


def day09A(input):
    heatmap = np.array([list(line) for line in input], dtype=int)
    minima = getMinima(heatmap)
    risk = [heatmap[x[0], x[1]] + 1 for x in minima]
    return sum(risk)


class Basin:
    def __init__(self, i, j, heatmap):
        self.i = i
        self.j = j
        self.__points = []
        self.__calculatePoints(heatmap)

    def __calculatePoints(self, heatmap):
        pointsToCheck = []
        pointsToCheck.append([self.i, self.j])

        while len(pointsToCheck) > 0:
            point = pointsToCheck.pop()
            if heatmap[point[0], point[1]] < 9 and point not in self.__points:
                self.__points.append(point)

                value = heatmap[point[0], point[1]]
                [left, right, up, down] = getSurroundingValues(heatmap, point[0], point[1])
                if point[0] > 0 and value < up:
                    pointsToCheck.append([point[0] - 1, point[1]])
                if point[0] < heatmap.shape[0] - 1 and value < down:
                    pointsToCheck.append([point[0] + 1, point[1]])
                if point[1] > 0 and value < left:
                    pointsToCheck.append([point[0], point[1] - 1])
                if point[1] < heatmap.shape[1] - 1 and value < right:
                    pointsToCheck.append([point[0], point[1] + 1])

    def size(self):
        return len(self.__points)


def day09B(input):
    heatmap = np.array([list(line) for line in input], dtype=int)
    minima = getMinima(heatmap)

    basins = [Basin(value[0], value[1], heatmap) for value in minima]

    sizes = [basin.size() for basin in basins]
    sizes.sort()

    return sizes[-1] * sizes[-2] * sizes[-3]


def main():
    example = readInputFromFile("day-09/example.txt")
    input = readInputFromFile("day-09/input.txt")

    print(f'Result example A: {day09A(example)}\n')
    print(f'Result puzzle data A: {day09A(input)}\n')
    print(f'Result example B: {day09B(example)}\n')
    print(f'Result puzzle data B: {day09B(input)}\n')


if __name__ == "__main__":
    main()
