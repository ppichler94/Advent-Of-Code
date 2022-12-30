from mylib.aoc_basics import Day
import nographs as nog


class PartA(Day):
    def parse(self, text, data):
        data.cubes = []
        for line in text.split("\n"):
            data.cubes.append(nog.Position([int(x) for x in line.split(",")]))
        data.moves = nog.Position.moves(3)

    def compute(self, data):
        return sum(0 if neighbor in data.cubes else 1
                   for cube in data.cubes
                   for neighbor in cube.neighbors(data.moves))

    def example_answer(self):
        return 64


class PartB(PartA):
    def compute(self, data):
        exterior_cubes = self.find_exterior_cubes(data)
        return sum(1 if neighbor in exterior_cubes else 0
                   for cube in data.cubes
                   for neighbor in cube.neighbors(data.moves))

    def find_exterior_cubes(self, data):
        def next_edges(cube, _):
            for target in cube.neighbors(data.moves, limits):
                yield target

        limit_min = [min(c[0] for c in data.cubes) - 1, min(c[1] for c in data.cubes) - 1, min(c[2] for c in data.cubes) - 1]
        limit_max = [max(c[0] for c in data.cubes) + 2, max(c[1] for c in data.cubes) + 2, max(c[2] for c in data.cubes) + 2]
        limits = [(limit_min[0], limit_max[0]), (limit_min[1], limit_max[1]), (limit_min[2], limit_max[2])]

        traversal = nog.TraversalBreadthFirst(next_edges)
        exterior_cubes = set(traversal.start_from(nog.Position(limit_min), already_visited=set(data.cubes)))

        return exterior_cubes

    def example_answer(self):
        return 58


Day.do_day(18, 2022, PartA, PartB)
