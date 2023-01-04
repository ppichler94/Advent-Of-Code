import numpy as np


def readInputFromFile(fileName):
    inputFile = open(fileName, "r")
    input = inputFile.readlines()
    input = [x.strip() for x in input]
    inputFile.close()
    return input


def createBoards(input):
    boards = []
    markedBoards = []
    index = 2
    while (index < len(input)):
        board = [x.split(" ") for x in input[index:index+5]]
        board = [[x for x in line if x] for line in board]
        boards.append(np.array(board, dtype=int))
        markedBoards.append(np.zeros([5, 5], dtype=int))
        index += 6

    return [boards, markedBoards]


def checkWinningCodition(markedBoard, markIndex):
    columnSum = np.sum(markedBoard, axis=0)[markIndex[1]]
    rowSum = np.sum(markedBoard, axis=1)[markIndex[0]]
    if ((columnSum.size > 0 and columnSum == 5)
            or (rowSum.size > 0 and rowSum == 5)):
        return True
    return False


def calculatePoints(board, markedBoard, number):
    unmarked = np.ma.array(board, mask=markedBoard)
    sumOfUnmarked = unmarked.sum()
    return sumOfUnmarked * number


def day04A(input):
    numbers = np.array(input[0].split(","), dtype=int)
    [boards, markedBoards] = createBoards(input)

    for number in numbers:
        for board, markedBoard in zip(boards, markedBoards):
            index = np.where(board == number)
            markedBoard[index] = 1
            winningBoard = checkWinningCodition(markedBoard, index)
            if (winningBoard):
                return calculatePoints(board, markedBoard, number)

    return 0


def day04B(input):
    numbers = np.array(input[0].split(","), dtype=int)
    [boards, markedBoards] = createBoards(input)
    lastWinningBoard = np.empty([5, 5])
    lastWinngingMarks = np.empty([5, 5])
    lastNumber = 0
    winningIndices = []

    for number in numbers:
        for i, (board, markedBoard) in enumerate(zip(boards, markedBoards)):
            if i in winningIndices:
                continue
            index = np.where(board == number)
            markedBoard[index] = 1
            winningBoard = checkWinningCodition(markedBoard, index)
            if (winningBoard):
                winningIndices.append(i)
                lastWinningBoard = board
                lastWinngingMarks = markedBoard
                lastNumber = number

    return calculatePoints(lastWinningBoard, lastWinngingMarks, lastNumber)


def main():
    example = readInputFromFile("day-04/example.txt")
    input = readInputFromFile("day-04/input.txt")

    print(f'Result example A: {day04A(example)}\n')
    print(f'Result puzzle data A: {day04A(input)}\n')
    print(f'Result example B: {day04B(example)}\n')
    print(f'Result puzzle data B: {day04B(input)}\n')


if __name__ == "__main__":
    main()
