from mylib.aoc_basics import Day
import nographs as nog


class Cube:
    def __init__(self, coordinates):
        self.x = int(coordinates[0])
        self.y = int(coordinates[1])
        self.z = int(coordinates[2])
        self.surface = 6

    def touches(self, cube):
        return abs(self.x - cube.x) + abs(self.y - cube.y) + abs(self.z - cube.z) == 1

    def neighbors(self):
        coordinates = [self.x, self.y, self.z]
        moves = nog.Position.moves(3)
        for move in moves:
            yield Cube([sum(x) for x in zip(coordinates, move)])

    def __repr__(self):
        return f"Cube(x={self.x}, y={self.y}, z={self.z}, surface={self.surface})"


class PartA(Day):
    def parse(self, text, data):
        data.cubes = []
        for line in text.split("\n"):
            data.cubes.append(Cube(line.split(",")))

    def compute(self, data):
        grid = []
        for new_cube in data.cubes:
            for cube in grid:
                if cube.touches(new_cube):
                    cube.surface -= 1
                    new_cube.surface -= 1
            grid.append(new_cube)
        return sum(cube.surface for cube in grid)

    def example_answer(self):
        return 64


class PartB(PartA):
    def compute(self, data):
        surface = 0
        exterior_cubes = self.find_exterior_cubes(data)
        exterior_cubes = [Cube(x) for x in exterior_cubes]
        for cube in data.cubes:
            for exterior_cube in exterior_cubes:
                if cube.touches(exterior_cube):
                    surface += 1
        return surface

    def find_exterior_cubes(self, data):
        def next_edges(cube, _):
            for target in cube.neighbors(moves, limits):
                yield target

        limit_min = [min(c.x for c in data.cubes) - 1, min(c.y for c in data.cubes) - 1, min(c.z for c in data.cubes) - 1]
        limit_max = [max(c.x for c in data.cubes) + 2, max(c.y for c in data.cubes) + 2, max(c.z for c in data.cubes) + 2]
        limits = [(limit_min[0], limit_max[0]), (limit_min[1], limit_max[1]), (limit_min[2], limit_max[2])]
        moves = nog.Position.moves(3)

        traversal = nog.TraversalBreadthFirst(next_edges)
        already_visited = set(nog.Position([c.x, c.y, c.z]) for c in data.cubes)
        exterior_cubes = set(traversal.start_from(nog.Position(limit_min), already_visited=already_visited))

        return exterior_cubes

    def example_answer(self):
        return 58


Day.do_day(18, 2022, PartA, PartB)
