import copy
import re
from collections import namedtuple
from functools import lru_cache
from mylib.aoc_basics import Day

Valve = namedtuple("Valve", ["name", "flow_rate", "links"])


class PartA(Day):
    def parse(self, text, data):
        data.valves = dict()
        for line in text.split("\n"):
            matcher = re.search("Valve (.*) has flow rate=(\d+); tunnels? leads? to valves? (.*)", line)
            if matcher:
                name = matcher.group(1)
                data.valves[name] = Valve(name, int(matcher.group(2)), matcher.group(3).split(", "))

    def compute(self, data):
        current_position = "AA"
        valve_map = dict()
        valve_map[current_position] = self.find_path(data.valves, current_position)
        for valve in [v.name for v in data.valves.values() if v.flow_rate > 0 and v.name]:
            valve_map[valve] = self.find_path(data.valves, valve)

        total_flow = self.find_solution(data.valves, [], current_position, 30, valve_map)
        return total_flow

    def find_solution(self, valves, open_valves, current_position, remaining_time, valve_map):
        current_flow_rate = 0

        if valves[current_position].flow_rate > 0:
            remaining_time -= 1
            current_flow_rate = valves[current_position].flow_rate * remaining_time
            open_valves.append(current_position)

        possible_next_valves = [v.name for v in valves.values() if v.flow_rate > 0 and v.name not in open_valves]
        if len(possible_next_valves) == 0:
            return current_flow_rate

        flow_rate = 0
        for next_valve in possible_next_valves:
            path_length = valve_map[current_position][next_valve]
            if path_length >= remaining_time:
                continue
            flow_rate = max(self.find_solution(valves, list(open_valves), next_valve, remaining_time - path_length, valve_map), flow_rate)
        return flow_rate + current_flow_rate

    def find_path(self, valves, start):
        to_do = [(start, 0)]
        distances = dict()
        distances[start] = 0
        while len(to_do) > 0 and len(distances) < len(valves):
            valve, length = to_do.pop(0)
            to_do.extend([(v, length + 1) for v in valves[valve].links])
            to_do = list(filter(lambda x: x[0] not in distances.keys(), to_do))
            if valve in distances:
                continue
            distances[valve] = length

        return distances

    def tests(self):
        yield self.test_solve(example), 1651, "example"


class PartB(PartA):

    def tests(self):
        yield self.test_solve(example), 1707, "example"


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
