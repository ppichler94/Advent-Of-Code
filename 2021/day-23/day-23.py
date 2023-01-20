import re
from mylib.aoc_basics import Day
import nographs as nog


class PartA(Day):
    def parse(self, text, data):
        data.rooms = ()
        data.room_index = {"A": 0, "B": 1, "C": 2, "D": 3}
        data.cost = {"A": 1, "B": 10, "C": 100, "D": 1000}
        data.end_rooms = (("A", "A"), ("B", "B"), ("C", "C"), ("D", "D"))
        pods = re.findall(r"[A-D]", text)
        data.start_rooms = tuple(zip(pods[:4], pods[4:]))
        data.valid_hallway_pos = (0, 1, 3, 5, 7, 9, 10)

    def compute(self, data):
        def next_edges(state, _):
            hallway, rooms = state
            # rooms = ((Front, Back), (Front, Back), ...)
            #          A               B

            hallway_pods = [(pod, i) for i, pod in enumerate(hallway) if pod]
            for pod, i in hallway_pods:
                if next_rooms := move_to_room(hallway_pods, rooms, i, pod):
                    next_hallway = tuple(p if i != j else None for j, p in enumerate(hallway))
                    steps = abs((2 + 2 * data.room_index[pod]) - i)
                    steps += 2 if next_rooms[data.room_index[pod]][0] is None else 1
                    yield (next_hallway, next_rooms), data.cost[pod] * steps
                    return

            for pod, i in [(front if front else back, i) for i, (front, back) in enumerate(rooms) if front or back]:
                if i == data.room_index[pod] and (rooms[i][1] == pod or rooms[i][0] == pod and rooms[i][1] == pod):
                    continue
                if next_rooms := move_to_room(hallway_pods, rooms, 2 + 2 * i, pod):
                    room = rooms[i]
                    next_room = (None, None) if room[0] is None else (None, room[1])
                    next_rooms = tuple(r if i != j else next_room for j, r in enumerate(next_rooms))
                    steps = abs((2 + 2 * i) - (2 + 2 * data.room_index[pod]))
                    steps += 2 if room[0] is None else 1
                    steps += 2 if rooms[data.room_index[pod]][1] is None else 1
                    yield (hallway, next_rooms), data.cost[pod] * steps
                    return

            for pod, room_idx in [(front if front is not None else back, room_idx) for room_idx, (front, back) in enumerate(rooms) if front or back]:
                for target in data.valid_hallway_pos:
                    pos = 2 + 2 * room_idx
                    if next_hallway := move_to_hallway(hallway, pod, pos, target):
                        room = rooms[room_idx]
                        next_room = (None, None) if room[0] is None else (None, room[1])
                        next_rooms = tuple(r if i != room_idx else next_room for i, r in enumerate(rooms))
                        steps = abs(pos - target)
                        steps += 2 if room[0] is None else 1
                        yield (next_hallway, next_rooms), data.cost[pod] * steps

        def move_to_room(hallway_pods, rooms, pos, pod):
            target = 2 + 2 * data.room_index[pod]
            low, high = (pos, target) if pos < target else (target, pos)
            if any(x in [i for pod, i in hallway_pods if i != pos] for x in list(range(low, high))):
                return None
            room = rooms[data.room_index[pod]]
            if room[1] is None:
                return tuple(x if i != data.room_index[pod] else (None, pod) for i, x in enumerate(rooms))
            if room[0] is None and room[1] == pod:
                return tuple(x if i != data.room_index[pod] else (pod, pod) for i, x in enumerate(rooms))
            return None

        def move_to_hallway(hallway, pod, pos, target):
            low, high = (pos, target + 1) if pos < target else (target, pos + 1)
            if any(x is not None for x in hallway[low:high]):
                return None
            return tuple(x if i != target else pod for i, x in enumerate(hallway))

        traversal = nog.TraversalShortestPaths(next_edges)
        for state in traversal.start_from((tuple([None] * 11), data.start_rooms)):
            hallway, rooms = state
            if rooms == data.end_rooms:
                return traversal.distance
        return "No result"

    def example_answer(self):
        return 12521


Day.do_day(23, 2021, PartA, None)
