import os
from typing import Tuple
from functools import lru_cache


class DeterministicDice:
    def __init__(self) -> None:
        self.counter = 0

    def roll(self) -> int:
        number = 1 + (self.counter % 100)
        self.counter += 1
        return number

    def get_roll_count(self) -> int:
        return self.counter


def read_input_from_file(file_name: str) -> list:
    script_path = os.path.dirname(os.path.abspath(__file__))
    input_file = open(f"{script_path}/{file_name}", "r")
    data = input_file.readlines()
    data = [x.strip() for x in data]
    input_file.close()
    return data


def update_position(position: int, count: int) -> int:
    position += count
    while position > 10:
        position -= 10
    return position


def move_player(position: int, points: int, dice: DeterministicDice) -> Tuple[int, int]:
    movement = sum(dice.roll() for _ in range(3))
    position = update_position(position, movement)
    points += position
    return (position, points)


@lru_cache(maxsize=None)
def do_quantum_turn(pos1: int, pos2: int, points1: int, points2: int) -> Tuple[int, int]:
    possibilities = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}

    wins1, wins2 = 0, 0

    for movement, splits in possibilities.items():
        pos = update_position(pos1, movement)
        points = points1 + pos
        if points >= 21:
            wins1 += splits
            continue
        pos = update_position(pos1, movement)
        next_wins2, next_wins1 = do_quantum_turn(pos2, pos, points2, points)
        wins1 += next_wins1 * splits
        wins2 += next_wins2 * splits

    return (wins1, wins2)


def get_starting_positions(data: list) -> Tuple[int, int]:
    a = int(data[0].split(": ")[1])
    b = int(data[1].split(": ")[1])
    return (a, b)


def part_1(data):
    position_a, position_b = get_starting_positions(data)
    points_a, points_b = 0, 0
    dice = DeterministicDice()
    while True:
        position_a, points_a = move_player(position_a, points_a, dice)
        if points_a >= 1000:
            return points_b * dice.get_roll_count()
        position_b, points_b = move_player(position_b, points_b, dice)
        if points_b >= 1000:
            return points_a * dice.get_roll_count()


def part_2(data):
    pos1, pos2 = get_starting_positions(data)
    wins = do_quantum_turn(pos1, pos2, 0, 0)
    print(f"Part 2: {wins}")


def main() -> None:
    data = read_input_from_file("input.txt")

    result_1 = part_1(data)
    print(f"Part 1: {result_1}")

    part_2(data)


if __name__ == "__main__":
    main()
