import functools

from mylib.aoc_basics import Day
import nographs as nog


class PartA(Day):
    def parse(self, text, data):
        valley = nog.Array(text.splitlines())
        moves = nog.Position.moves(zero_move=True)
        limits = valley.limits()

        def blizzard_generator():
            blizzard_limits = [(1, size - 1) for size in valley.size()]
            blizzard_movements = {">": (0, 1), "^": (-1, 0), "<": (0, -1), "v": (1, 0)}
            blizzard_pos_and_dir = tuple((pos, blizzard_movements[c])
                                         for c in blizzard_movements
                                         for pos in valley.findall(c))
            blizzard_positions = tuple(pos for pos, direction in blizzard_pos_and_dir)
            blizzard_directions = [direction for pos, direction in blizzard_pos_and_dir]
            while True:
                blizzard_positions = tuple((pos + direction).wrap_to_cuboid(blizzard_limits)
                                           for pos, direction in zip(blizzard_positions, blizzard_directions))
                yield set(blizzard_positions)

        blizzard_iter = iter(blizzard_generator())

        @functools.cache
        def blizzards(minute):
            return next(blizzard_iter)

        def next_edges(state, _):
            position, minute = state
            next_minute = minute + 1
            blizzard_positions = blizzards(minute)
            for next_position in position.neighbors(moves, limits):
                if valley[next_position] != "#" and next_position not in blizzard_positions:
                    yield (next_position, next_minute), 1

        data.start = nog.Position.at(0, 1)
        data.target = nog.Position(valley.size()) + (-1, -2)
        data.traversal = nog.TraversalAStar(next_edges)

    @classmethod
    def heuristic(cls, target):
        def distance(state):
            pos, minute = state
            return pos.manhattan_distance(target)
        return distance

    def compute(self, data):
        for position, minute in data.traversal.start_from(self.heuristic(data.target), (data.start, 0)):
            if position == data.target:
                return data.traversal.depth

    def example_answer(self):
        return 18

    def get_example_input(self, puzzle):
        return '''
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
'''


class PartB(PartA):
    def compute(self, data):
        result = 0
        minute = 0
        paths = [(data.start, data.target), (data.target, data.start), (data.start, data.target)]
        for start, target in paths:
            for position, minute in data.traversal.start_from(self.heuristic(target), (start, minute)):
                if position == target:
                    result += data.traversal.depth
                    break

        return result

    def example_answer(self):
        return 54


Day.do_day(24, 2022, PartA, PartB)
