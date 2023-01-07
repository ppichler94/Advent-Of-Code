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
        #                       R,      D,       L,      U
        data.directions = ((0, 1), (1, 0), (0, -1), (-1, 0))
        data.direction_index = 0

    def compute(self, data):
        for instruction in data.instructions:
            match instruction:
                case "R":
                    data.direction_index = (data.direction_index + 1) % 4
                case "L":
                    data.direction_index = (data.direction_index - 1) % 4
                case count:
                    for _ in range(int(count)):
                        stuck = self.move(data, data.direction_index)
                        if stuck:
                            break
        return 1000 * data.position[0] + 4 * data.position[1] + data.direction_index

    def move(self, data, direction_index):
        direction = data.directions[direction_index]
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


class PartB(PartA):
    def part_config(self, data):
        max_map_length = max(upper for lower, upper in data.map.limits()) - 2
        data.edge_length = max_map_length // 4

        wrapping_number = 1 if data.config is not None else 0

        # Wrapping per move from one "open" edge to the other.
        # Elements: map_y, map_x, facing -> map_y, map_x, facing
        data.wrapping = ({
                        # wrapping definition for input data
                        # 0 degrees
                        (0, 2, 3): [3, 0, 3],
                        # 90 degrees
                        (0, 1, 3): [3, 0, 0],
                        (2, 0, 3): [1, 1, 0],
                        (0, 2, 1): [1, 1, 2],
                        (2, 1, 1): [3, 0, 2],
                        # 180 degrees
                        (2, 0, 2): [0, 1, 0],
                        (0, 2, 0): [2, 1, 2],
                    }, {
                        # wrapping definition for example data
                        # 90 degrees
                        (1, 2, 0): [2, 3, 1],
                        (0, 2, 2): [1, 1, 1],
                        (2, 3, 1): [1, 0, 0],
                        (1, 1, 1): [2, 2, 0],
                        # 180 degrees
                        (0, 2, 3): [1, 0, 1],
                        (0, 2, 0): [2, 3, 2],
                        (2, 2, 1): [1, 0, 3],
                    })[wrapping_number]
        wrapping_items = list(data.wrapping.items())
        data.wrapping.update(  # add symmetric edge change, with reversed directions
            ((to_map_y, to_map_x, (to_dir + 2) % 4), (from_map_y, from_map_x, (from_dir + 2) % 4))
            for (from_map_y, from_map_x, from_dir), (to_map_y, to_map_x, to_dir)
            in wrapping_items)

    def move(self, data, direction_index):
        direction = data.directions[direction_index]
        next_position = data.position + direction
        next_character = data.map[next_position]
        next_direction_index = direction_index
        if next_character == " ":
            face_y, face_x = ((coordinate - 1) // data.edge_length for coordinate in data.position)
            face_y, face_x, next_direction_index = data.wrapping[(face_y, face_x, direction_index)]
            y_on_face, x_on_face = ((coordinate - 1) % data.edge_length for coordinate in next_position)
            for _ in range(next_direction_index - direction_index if direction_index <= next_direction_index
                           else next_direction_index + 4 - direction_index):
                y_on_face, x_on_face = x_on_face, y_on_face
                x_on_face = data.edge_length - 1 - x_on_face
            next_position = nog.Position.at((face_y * data.edge_length + y_on_face + 1),
                                            (face_x * data.edge_length + x_on_face + 1))
            next_character = data.map[next_position]
        if next_character == "#":
            return True
        data.position = next_position
        data.direction_index = next_direction_index

    def example_answer(self):
        return 5031


Day.do_day(22, 2022, PartA, PartB)
