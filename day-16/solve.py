import itertools
import re
from collections import namedtuple
from mylib.aoc_basics import Day
import nographs as nog

Valve = namedtuple("Valve", ["name", "flow_rate", "links"])


class PartA(Day):
    def parse(self, text, data):
        data.valves = dict()
        for line in text.split("\n"):
            matcher = re.search("Valve (.*) has flow rate=(\d+); tunnels? leads? to valves? (.*)", line)
            if matcher:
                name = matcher.group(1)
                data.valves[name] = Valve(name, int(matcher.group(2)), matcher.group(3).split(", "))
        data.valves_to_open = frozenset(v.name for v in data.valves.values() if v.flow_rate > 0)
        data.max_flow_rate = sum(v.flow_rate for v in data.valves.values())

        def next_edges(state, _):
            valve, closed, flow_rate = state
            if valve in closed:
                yield (valve, closed.difference([valve]), flow_rate + data.valves[valve].flow_rate), data.max_flow_rate - flow_rate
            for target in data.valves[valve].links:
                yield (target, closed, flow_rate), data.max_flow_rate - flow_rate

        data.next_edges = next_edges

    def compute(self, data):
        start_valve = "AA"
        time_limit = 30

        traversal = nog.TraversalShortestPaths(data.next_edges)
        for state in traversal.start_from((start_valve, data.valves_to_open, 0)):
            valve, closed, flow_rate = state
            if traversal.depth == time_limit or not closed:
                return data.max_flow_rate * time_limit - traversal.distance

    def example_answer(self):
        return 1651


class PartB(PartA):
    def compute(self, data):
        def next_edges_group(state, _):
            my_position, elephant_position, closed, flow_rate = state
            for my_next, elephant_next in itertools.product(
                next_edges((my_position, closed, flow_rate), _),
                next_edges((elephant_position, closed, flow_rate), _)
            ):
                (my_target, my_closed, my_flow_rate), weight = my_next
                (elephant_target, elephant_closed, elephant_flow_rate), weight = elephant_next
                if my_closed != elephant_closed or my_closed == closed:
                    yield (my_target, elephant_target, my_closed.intersection(elephant_closed),
                           my_flow_rate + elephant_flow_rate - flow_rate), weight

        start_valve = "AA"
        time_limit = 26
        next_edges = data.next_edges
        traversal = nog.TraversalShortestPaths(next_edges_group)
        for state in traversal.start_from((start_valve, start_valve, data.valves_to_open, 0)):
            my_valve, elephant_valve, closed, flow_rate = state
            if traversal.depth == time_limit or not closed:
                return data.max_flow_rate * time_limit - traversal.distance

    def example_answer(self):
        return 1707


example = ''''
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
'''

Day.do_day(16, 2022, PartA, PartB)
