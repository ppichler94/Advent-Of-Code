import functools
import re
from mylib.aoc_basics import Day
import nographs as nog


class PartA(Day):
    def parse(self, text, data):
        data.room_index = {"A": 0, "B": 1, "C": 2, "D": 3}
        data.cost = {"A": 1, "B": 10, "C": 100, "D": 1000}
        data.end_rooms = (("A", "A"), ("B", "B"), ("C", "C"), ("D", "D"))
        pods = re.findall(r"[A-D]", text)
        data.start_rooms = tuple(zip(pods[:4], pods[4:]))
        data.valid_hallway_pos = (0, 1, 3, 5, 7, 9, 10)

    def compute(self, data):
        def next_edges(state, _):
            hallway, rooms = state

            hallway_pods = [(pod, i) for i, pod in enumerate(hallway) if pod]
            for pod, i in hallway_pods:
                if result := self.move_hallway_to_room(data, hallway, rooms, (0, i)):
                    next_rooms, next_hallway, cost = result
                    yield (next_hallway, next_rooms), cost
                    return

            for pod, room_x, room_y in self.iterate_rooms(rooms):
                if room_x == data.room_index[pod] and not any(x != pod for x in rooms[room_x] if x):
                    continue
                if result := self.move_room_to_room(data, hallway, rooms, (room_y, 2 + 2 * room_x)):
                    next_rooms, cost = result
                    yield (hallway, next_rooms), cost
                    return

            for pod, room_x, room_y in self.iterate_rooms(rooms):
                if room_x == data.room_index[pod] and not any(x != pod for x in rooms[room_x] if x):
                    continue
                for target in data.valid_hallway_pos:
                    pos = 2 + 2 * room_x
                    start = (room_y, pos)
                    if result := self.move_room_to_hallway(data, hallway, rooms, start, (0, target)):
                        next_rooms, next_hallway, cost = result
                        yield (next_hallway, next_rooms), cost

        traversal = nog.TraversalShortestPaths(next_edges)
        for state in traversal.start_from((tuple([None] * 11), data.start_rooms)):
            hallway, rooms = state
            if rooms == data.end_rooms:
                return traversal.distance
        return "No result"

    @staticmethod
    def iterate_rooms(rooms):
        for room_x, room in list(enumerate(rooms)):
            for room_y, pod in enumerate(room):
                if pod:
                    yield pod, room_x, room_y + 1
                    break

    def move_hallway_to_room(self, data, hallway, rooms, start):
        pod = hallway[start[1]]
        room_id = data.room_index[pod]
        end = (0, 2 + 2 * room_id)
        if self.hallway_blocked(hallway, start[1], end[1]):
            return None
        room = rooms[room_id]
        if any(x != pod for x in room if x):
            return None
        end_y = len(room) - list(reversed(room)).index(None) - 1
        next_room = tuple([None] * end_y + [pod] * (len(room) - end_y))
        next_rooms = tuple(x if i != room_id else next_room for i, x in enumerate(rooms))
        next_hallway = tuple(x if i != start[1] else None for i, x in enumerate(hallway))
        return next_rooms, next_hallway, self.calculate_cost(data.cost[pod], start, (end_y + 1, end[1]))

    def move_room_to_room(self, data, hallway, rooms, start):
        start_room_id = (start[1] - 2) // 2
        pod = rooms[start_room_id][start[0] - 1]
        end_room_id = data.room_index[pod]
        end = (0, 2 + 2 * end_room_id)
        if self.hallway_blocked(hallway, start[1], end[1]):
            return None
        end_room = rooms[end_room_id]
        if any(x != pod for x in end_room if x):
            return None
        end_y = len(end_room) - list(reversed(end_room)).index(None) - 1
        next_end_room = tuple([None] * end_y + [pod] * (len(end_room) - end_y))
        next_start_room = tuple([None] * (start[0]) + list(rooms[start_room_id][(start[0]) :]))
        next_rooms = tuple(
            next_end_room if i == end_room_id else next_start_room if i == start_room_id else x
            for i, x in enumerate(rooms)
        )
        return next_rooms, self.calculate_cost(data.cost[pod], start, (end_y + 1, end[1]))

    def move_room_to_hallway(self, data, hallway, rooms, start, end):
        if self.hallway_blocked(hallway, start[1], end[1]):
            return None
        room_id = (start[1] - 2) // 2
        pod = rooms[room_id][start[0] - 1]
        next_hallway = tuple(x if i != end[1] else pod for i, x in enumerate(hallway))
        next_room = tuple([None] * (start[0]) + list(rooms[room_id][start[0] :]))
        next_rooms = tuple(x if i != room_id else next_room for i, x in enumerate(rooms))
        return next_rooms, next_hallway, self.calculate_cost(data.cost[pod], start, end)

    @staticmethod
    def hallway_blocked(hallway, start, end):
        low, high = (start + 1, end) if start < end else (end + 1, start)
        return any(x is not None for x in hallway[low:high])

    @staticmethod
    def calculate_cost(cost, start, end):
        return cost * (start[0] + end[0] + abs(start[1] - end[1]))

    def example_answer(self):
        return 12521


class PartB(PartA):
    def part_config(self, data):
        data.end_rooms = (("A", "A"), ("B", "B"), ("C", "C"), ("D", "D"))
        data.end_rooms = (tuple(["A"] * 4), tuple(["B"] * 4), tuple(["C"] * 4), tuple(["D"] * 4))
        data.start_rooms = (
            (data.start_rooms[0][0], "D", "D", data.start_rooms[0][1]),
            (data.start_rooms[1][0], "C", "B", data.start_rooms[1][1]),
            (data.start_rooms[2][0], "B", "A", data.start_rooms[2][1]),
            (data.start_rooms[3][0], "A", "C", data.start_rooms[3][1]),
        )

    def example_answer(self):
        return 44169


Day.do_day(23, 2021, PartA, PartB)
