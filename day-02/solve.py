from enum import IntEnum


class Shape(IntEnum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class Outcome(IntEnum):
    WIN = 6
    DRAW = 3
    LOSS = 0


def main():
    example_data = read_input_from_file("day-02/example.txt")
    input_data = read_input_from_file("day-02/input.txt")

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
    score = 0
    for line in input:
        codes = line.split(" ")
        opponent_shape = get_shape(codes[0])
        player_shape = get_shape(codes[1])
        score += calculate_score(opponent_shape, player_shape)
    return score


def get_shape(code):
    if code == "A" or code == "X":
        return Shape.ROCK
    if code == "B" or code == "Y":
        return Shape.PAPER
    if code == "C" or code == "Z":
        return Shape.SCISSORS


def calculate_score(opponent_shape, player_shape):
    score = player_shape
    if is_draw(opponent_shape, player_shape):
        score += 3
    elif is_win(opponent_shape, player_shape):
        score += 6
    return score


def is_draw(opponent_shape, player_shape):
    return opponent_shape == player_shape


def is_win(opponent_shape, player_shape):
    if player_shape == Shape.ROCK and opponent_shape == Shape.SCISSORS:
        return True
    if player_shape == Shape.PAPER and opponent_shape == Shape.ROCK:
        return True
    if player_shape == Shape.SCISSORS and opponent_shape == Shape.PAPER:
        return True
    return False


def solve_b(input):
    score = 0
    for line in input:
        codes = line.split(" ")
        opponent_shape = get_shape(codes[0])
        outcome = get_outcome(codes[1])
        player_shape = calculate_shape(opponent_shape, outcome)
        score += (player_shape + outcome)
    return score


def get_outcome(code):
    if code == "X":
        return Outcome.LOSS
    if code == "Y":
        return Outcome.DRAW
    if code == "Z":
        return Outcome.WIN


def calculate_shape(opponent_shape, outcome):
    if outcome == Outcome.DRAW:
        return opponent_shape
    if opponent_shape == Shape.ROCK:
        return Shape.PAPER if outcome == Outcome.WIN else Shape.SCISSORS
    if opponent_shape == Shape.PAPER:
        return Shape.SCISSORS if outcome == Outcome.WIN else Shape.ROCK
    if opponent_shape == Shape.SCISSORS:
        return Shape.ROCK if outcome == Outcome.WIN else Shape.PAPER


if __name__ == "__main__":
    main()
