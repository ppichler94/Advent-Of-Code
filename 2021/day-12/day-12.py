import functools
import itertools

import nographs as nog
from mylib.aoc_basics import Day


class PartA(Day):
    def parse(self, text, data):
        def visit_allowed(pos, visited):
            return pos != pos.lower() or pos not in visited

        raw_edges = [line.split("-") for line in text.splitlines()]
        raw_edges.extend([[x[1], x[0]] for x in raw_edges])
        raw_edges = sorted(raw_edges)
        data.edges = dict([k, list(map(lambda x: x[1], v))] for k, v in itertools.groupby(raw_edges, lambda x: x[0]))
        data.is_visit_allowed = visit_allowed

    def compute(self, data):
        def next_edges(state, _):
            pos, visited = state
            if pos == "end":
                return
            for next_pos in data.edges[pos]:
                if data.is_visit_allowed(next_pos, visited):
                    yield next_pos, visited + (next_pos,)

        traversal = nog.TraversalBreadthFirst(next_edges)
        traversal.start_from(("start", ("start",)), build_paths=True)
        return sum(1 if pos == "end" else 0 for pos, visited in traversal)

    def example_answer(self):
        return 10


class PartB(PartA):
    def part_config(self, data):
        def visit_allowed(pos, visited):
            if pos == "start" and pos in visited:
                return False
            if pos != pos.lower():
                return True
            visited_small_caves = tuple(filter(lambda x: x == x.lower(), visited))
            sums = {x: visited_small_caves.count(x) for x in visited_small_caves}
            small_caves_visited_two_times = sum(v == 2 for v in sums.values())
            if small_caves_visited_two_times == 1:
                if pos in sums:
                    return sums[pos] < 1
                else:
                    return True
            if small_caves_visited_two_times == 0:
                return True
        data.is_visit_allowed = visit_allowed

    def example_answer(self):
        return 36


Day.do_day(12, 2021, PartA, PartB)
