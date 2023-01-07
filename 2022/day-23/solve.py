import itertools
from mylib.aoc_basics import Day
import nographs as nog


class PartA(Day):
    def parse(self, text, data):
        grove = nog.Array(text.splitlines())
        data.elfs = set(grove.findall("#"))
        data.directions = [
            ((-1, -1), (-1, +0), (-1, +1)),
            ((+1, -1), (+1, +0), (+1, +1)),
            ((-1, -1), (+0, -1), (+1, -1)),
            ((-1, +1), (+0, +1), (+1, +1)),
        ]

    @staticmethod
    def do_round(elfs, directions):
        propositions = dict()
        for elf in elfs:
            if all(elf + direction not in elfs
                   for direction_list in directions
                   for direction in direction_list):
                continue
            for direction_list in directions:
                if all(elf + direction not in elfs
                       for direction in direction_list):
                    new_pos = elf + direction_list[1]
                    if new_pos in propositions:
                        propositions[new_pos] = None
                    else:
                        propositions[new_pos] = elf
                    break

        any_elf_moving = False
        for proposition, elf in propositions.items():
            if elf is not None:
                elfs.discard(elf)
                elfs.add(proposition)
                any_elf_moving = True
        first_direction = directions.pop(0)
        directions.append(first_direction)
        return any_elf_moving

    @staticmethod
    def find_min_max(elfs):
        min_y = min(elf[0] for elf in elfs)
        max_y = max(elf[0] for elf in elfs)
        min_x = min(elf[1] for elf in elfs)
        max_x = max(elf[1] for elf in elfs)
        return min_x, max_x, min_y, max_y

    def compute(self, data):
        for _ in range(10):
            self.do_round(data.elfs, data.directions)

        min_x, max_x, min_y, max_y = self.find_min_max(data.elfs)
        return (max_x + 1 - min_x) * (max_y + 1 - min_y) - len(data.elfs)

    def example_answer(self):
        return 110


class PartB(PartA):
    def compute(self, data):
        for round_number in itertools.count(1):
            moving = self.do_round(data.elfs, data.directions)
            if not moving:
                break

        return round_number

    def example_answer(self):
        return 20


Day.do_day(23, 2022, PartA, PartB)
