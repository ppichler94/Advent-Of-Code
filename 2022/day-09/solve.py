import numpy as np
from mylib.aoc_basics import Day


class PartA(Day):
    def part_config(self, data):
        data.knots = [np.zeros(2, dtype=int) for _ in range(1)]

    def compute(self, data):
        visited = set()
        head_pos = np.zeros(2, dtype=int)
        for line in data.text.splitlines():
            PartA.execute_motion(line, visited, head_pos, data.knots)
        return len(visited)

    @staticmethod
    def execute_motion(motion, visited, head_pos, knots):
        motion_parts = motion.split(" ")
        direction = motion_parts[0]
        count = int(motion_parts[1])
        for _ in range(count):
            PartA.execute_step(direction, visited, head_pos, knots)

    @staticmethod
    def execute_step(direction, visited, head_pos, knots):
        match direction:
            case "U":
                head_pos[1] += 1
            case "D":
                head_pos[1] -= 1
            case "R":
                head_pos[0] += 1
            case "L":
                head_pos[0] -= 1
        PartA.update_tail_pos(head_pos, knots[0])
        for i in range(1, len(knots)):
            changed = PartA.update_tail_pos(knots[i - 1], knots[i])
            if not changed:
                break
        visited.add(f'{knots[-1][0]}.{knots[-1][1]}')

    @staticmethod
    def update_tail_pos(head_pos, tail_pos):
        diff = head_pos - tail_pos
        if np.linalg.norm(diff) < 2:
            return False
        if np.linalg.norm(diff) == 2:
            diff = diff / np.linalg.norm(diff)
        if np.linalg.norm(diff) > 2:
            diff = np.divide(diff, np.absolute(diff))
        tail_pos += np.rint(diff).astype(int)
        return True

    def example_answer(self):
        return 13

    def get_example_input(self, puzzle):
        return """
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
"""


class PartB(PartA):
    def part_config(self, data):
        data.knots = [np.zeros(2, dtype=int) for _ in range(9)]

    def example_answer(self):
        return 1

    def tests(self):
        yield example2, 36, "Larger example"


example2 = """
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
"""


Day.do_day(9, 2022, PartA, PartB)
