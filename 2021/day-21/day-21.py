from typing import Tuple
import functools
from mylib.aoc_basics import Day


class DeterministicDice:
    def __init__(self) -> None:
        self.counter = 0

    def roll(self) -> int:
        number = 1 + (self.counter % 100)
        self.counter += 1
        return number

    def get_roll_count(self) -> int:
        return self.counter


class PartA(Day):
    def parse(self, text, data):
        lines = text.splitlines()
        data.position_a = int(lines[0].split(": ")[1])
        data.position_b = int(lines[1].split(": ")[1])

    def compute(self, data):
        position_a, position_b = data.position_a, data.position_b
        points_a, points_b = 0, 0
        dice = DeterministicDice()
        while True:
            position_a, points_a = self.move_player(position_a, points_a, dice)
            if points_a >= 1000:
                return points_b * dice.get_roll_count()
            position_b, points_b = self.move_player(position_b, points_b, dice)
            if points_b >= 1000:
                return points_a * dice.get_roll_count()

    @staticmethod
    def move_player(position: int, points: int, dice: DeterministicDice) -> Tuple[int, int]:
        movement = sum(dice.roll() for _ in range(3))
        position = (position + movement - 1) % 10 + 1
        points += position
        return position, points

    def example_answer(self):
        return 739785


class PartB(PartA):
    def compute(self, data):
        wins = self.do_quantum_turn(data.position_a, data.position_b, 0, 0)
        return max(wins)

    @classmethod
    @functools.cache
    def do_quantum_turn(cls, pos1: int, pos2: int, points1: int, points2: int) -> Tuple[int, int]:
        possibilities = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}
        wins1, wins2 = 0, 0

        for movement, splits in possibilities.items():
            pos = (pos1 + movement - 1) % 10 + 1
            points = points1 + pos
            if points >= 21:
                wins1 += splits
                continue
            pos = (pos1 + movement - 1) % 10 + 1
            next_wins2, next_wins1 = cls.do_quantum_turn(pos2, pos, points2, points)
            wins1 += next_wins1 * splits
            wins2 += next_wins2 * splits

        return wins1, wins2

    def example_answer(self):
        return 444356092776315


Day.do_day(21, 2021, PartA, PartB)
