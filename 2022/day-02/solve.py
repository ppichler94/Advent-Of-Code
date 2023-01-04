from enum import IntEnum
from mylib.aoc_basics import Day


class Shape(IntEnum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class Outcome(IntEnum):
    WIN = 6
    DRAW = 3
    LOSS = 0


class PartA(Day):
    def parse(self, text, data):
        data.lines = text.splitlines()

    def compute(self, data):
        score = 0
        for line in data.lines:
            codes = line.split(" ")
            opponent_shape = self.get_shape(codes[0])
            player_shape = self.get_shape(codes[1])
            score += self.calculate_score(opponent_shape, player_shape)
        return score

    def get_shape(self, code):
        if code == "A" or code == "X":
            return Shape.ROCK
        if code == "B" or code == "Y":
            return Shape.PAPER
        if code == "C" or code == "Z":
            return Shape.SCISSORS

    def calculate_score(self, opponent_shape, player_shape):
        score = player_shape
        if self.is_draw(opponent_shape, player_shape):
            score += Outcome.DRAW
        elif self.is_win(opponent_shape, player_shape):
            score += Outcome.WIN
        return score

    def is_draw(self, opponent_shape, player_shape):
        return opponent_shape == player_shape

    def is_win(self, opponent_shape, player_shape):
        if player_shape == Shape.ROCK and opponent_shape == Shape.SCISSORS:
            return True
        if player_shape == Shape.PAPER and opponent_shape == Shape.ROCK:
            return True
        if player_shape == Shape.SCISSORS and opponent_shape == Shape.PAPER:
            return True
        return False


class PartB(PartA):
    def compute(self, data):
        score = 0
        for line in data.lines:
            codes = line.split(" ")
            opponent_shape = self.get_shape(codes[0])
            outcome = self.get_outcome(codes[1])
            player_shape = self.calculate_shape(opponent_shape, outcome)
            score += (player_shape + outcome)
        return score


    def get_outcome(self, code):
        if code == "X":
            return Outcome.LOSS
        if code == "Y":
            return Outcome.DRAW
        if code == "Z":
            return Outcome.WIN

    def calculate_shape(self, opponent_shape, outcome):
        if outcome == Outcome.DRAW:
            return opponent_shape
        if opponent_shape == Shape.ROCK:
            return Shape.PAPER if outcome == Outcome.WIN else Shape.SCISSORS
        if opponent_shape == Shape.PAPER:
            return Shape.SCISSORS if outcome == Outcome.WIN else Shape.ROCK
        if opponent_shape == Shape.SCISSORS:
            return Shape.ROCK if outcome == Outcome.WIN else Shape.PAPER


Day.do_day(2, 2022, PartA, PartB)
