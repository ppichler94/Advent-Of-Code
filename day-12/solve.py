import numpy as np
from mylib.aoc_basics import Day
import nographs as nog


class PartA(Day):
    def part_config(self, data):
        data.start = "S"

    def compute(self, data):
        hills_map = nog.Array(data.text.splitlines())
        limits = hills_map.limits()
        moves = nog.Position.moves()

        def next_edges(position, _):
            for target in position.neighbors(moves, limits):
                if PartA.elevation(hills_map[target]) <= PartA.elevation(hills_map[position]) + 1:
                    yield target

        start = hills_map.findall(data.start)
        end = hills_map.findall("E")[0]

        traversal = nog.TraversalBreadthFirst(next_edges).start_from(start_vertices=start)
        traversal.go_to(end)
        return traversal.depth

    @staticmethod
    def elevation(character):
        character = {"S": "a", "E": "z"}.get(character, character)
        return ord(character) - ord("a")


    def example_answer(self):
        return 31


class PartB(PartA):
    def part_config(self, data):
        data.start = "a"

    def example_answer(self):
        return 29


Day.do_day(12, 2022, PartA, PartB)
