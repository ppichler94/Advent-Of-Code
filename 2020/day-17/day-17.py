from functools import partial
from itertools import chain
from mylib.aoc_basics import Day
import nographs as nog


class PartA(Day):
    def parse(self, text, data):
        initial_state = nog.Array(text.splitlines())
        data.initial_state = initial_state.findall("#")
        data.dimension = 3

    def compute(self, data):
        moves = nog.Position.moves(data.dimension, diagonals=True)
        active_cubes = set([nog.Position.at(c[0], c[1], *[0] * (data.dimension - 2)) for c in data.initial_state])
        for _ in range(6):
            to_deactivate = set(filter(partial(self.is_to_deactivate, moves, active_cubes), active_cubes))
            to_activate = set(
                filter(
                    lambda neighbor: len([n for n in neighbor.neighbors(moves) if n in active_cubes]) == 3,
                    chain.from_iterable(cube.neighbors(moves) for cube in active_cubes),
                )
            )

            active_cubes -= to_deactivate
            active_cubes.update(to_activate)

        return len(active_cubes)

    @staticmethod
    def is_to_deactivate(moves, active_cubes, cube):
        active_neighbors = len([n for n in cube.neighbors(moves) if n in active_cubes])
        return active_neighbors < 2 or active_neighbors > 3

    def example_answer(self):
        return 112


class PartB(PartA):
    def part_config(self, data):
        data.dimension = 4

    def example_answer(self):
        return 848


Day.do_day(17, 2020, PartA, PartB)
