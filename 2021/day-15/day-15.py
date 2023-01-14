import numpy as np
from mylib.aoc_basics import Day
import nographs as nog


class PartA(Day):
    def parse(self, text, data):
        def risk_at_pos(pos):
            return data.cave[pos]

        data.cave = nog.Array([[int(x) for x in line] for line in text.splitlines()])
        data.limits = data.cave.limits()
        data.moves = nog.Position.moves()
        data.start = nog.Position.at(0, 0)
        data.end = nog.Position.at(data.limits[0][1] - 1, data.limits[1][1] - 1)
        data.risk_at_pos = risk_at_pos

    def compute(self, data):
        def next_edges(pos: nog.Position, _):
            for next_pos in pos.neighbors(data.moves, data.limits):
                yield next_pos, data.risk_at_pos(next_pos)

        def heuristic(pos):
            return pos.manhattan_distance(data.end)

        traversal = nog.TraversalAStar(next_edges)
        found = traversal.start_from(heuristic, data.start).go_to(data.end)
        return traversal.distances[found]

    def example_answer(self):
        return 40


class PartB(PartA):
    def part_config(self, data):
        def risk_at_pos(pos):
            block_y, y = divmod(pos[0], block_size_y)
            block_x, x = divmod(pos[1], block_size_x)
            return (data.cave[(y, x)] + block_x + block_y - 1) % 9 + 1

        block_size_y = data.limits[0][1]
        block_size_x = data.limits[1][1]
        data.limits = [(0, block_size_y * 5), (0, block_size_x * 5)]
        data.end = nog.Position.at(data.limits[0][1] - 1, data.limits[1][1] - 1)

        data.risk_at_pos = risk_at_pos

    def example_answer(self):
        return 315


Day.do_day(15, 2021, PartA, PartB)
