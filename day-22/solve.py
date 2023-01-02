import re
import nographs as nog
from mylib.aoc_basics import Day


class PartA(Day):
    def parse(self, text, data):
        map_text, instructions_text = text.split("\n\n")
        map_lines = map_text.splitlines()
        max_x = max(len(line) for line in map_lines)
        map_lines_filled = [" " + line + " " * (max_x - len(line) + 1) for line in map_lines]
        empty_line = " " * (max_x + 2)
        map_lines_filled = [empty_line] + map_lines_filled + [empty_line]
        data.map = nog.Array(map_lines_filled)
        data.instructions = re.split("([RL])", instructions_text)
        start_x = map_lines_filled[1].index('.')
        data.position = nog.Position.at(1, start_x)

    def compute(self, data):
        directions = ((0, 1), (1, 0), (0, -1), (-1, 0))
        direction_index = 0
        for instruction in data.instructions:
            match instruction:
                case "R":
                    direction_index = (direction_index + 1) % 4
                case "L":
                    direction_index = (direction_index - 1) % 4
                case count:
                    for _ in range(int(count)):
                        stuck = self.move(data, directions[direction_index])
                        if stuck:
                            break
        return 1000 * data.position[0] + 4 * data.position[1] + direction_index

    def move(self, data, direction):
        next_position = data.position + direction
        next_character = data.map[next_position]
        if next_character == " ":
            back_direction = [-x for x in direction]
            while data.map[next_position + back_direction] != " ":
                next_position += back_direction
        if next_character == "#":
            return True
        data.position = next_position

    def example_answer(self):
        return 6032


class PartB(Day):
    pass


Day.do_day(22, 2022, PartA, PartB)
