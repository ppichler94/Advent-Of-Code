import nographs as nog
from mylib.aoc_basics import Day


class PartA(Day):
    def parse(self, text, data):
        data.heightmap = nog.Array([[int(x) for x in list(line)] for line in text.splitlines()])
        data.moves = nog.Position.moves()
        data.limits = data.heightmap.limits()

    def compute(self, data):
        minima = self.get_minima(data)
        return sum(data.heightmap[x] + 1 for x in minima)

    @staticmethod
    def get_minima(data):
        minima = []
        for y in range(data.limits[0][1]):
            for x in range(data.limits[1][1]):
                pos = nog.Position.at(y, x)
                neighbors = [data.heightmap[x] for x in pos.neighbors(data.moves, data.limits)]
                if all(data.heightmap[pos] < v for v in neighbors):
                    minima.append(pos)
        return minima

    def example_answer(self):
        return 15


class PartB(PartA):
    def compute(self, data):
        minima = self.get_minima(data)

        sizes = [self.get_basin_size(data, pos) for pos in minima]
        sizes.sort()

        return sizes[-1] * sizes[-2] * sizes[-3]

    @staticmethod
    def get_basin_size(data, position):
        def next_edges(pos, _):
            for next_pos in pos.neighbors(data.moves, data.limits):
                if data.heightmap[pos] < data.heightmap[next_pos] < 9:
                    yield next_pos

        traversal = nog.TraversalBreadthFirst(next_edges)
        return len(set(traversal.start_from(position, already_visited=set()))) + 1

    def example_answer(self):
        return 1134


Day.do_day(9, 2021, PartA, PartB)
