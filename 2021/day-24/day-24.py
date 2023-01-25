import functools
from mylib.aoc_basics import Day


class PartA(Day):
    def parse(self, text, data):
        instructions = text.splitlines()
        part_length = len(instructions) // 14
        data.block_params = [
            [int(instructions[part + offset].split(" ")[2]) for offset in (4, 5, 15)]
            for part in range(0, 14 * part_length, part_length)
        ]

    def compute(self, data):
        return self.find_number(data.block_params, True)

    @staticmethod
    def find_number(block_parameters, search_down):
        @functools.cache
        def find_next(z, digit_index):
            for digit in range(9, 0, -1) if search_down else range(1, 10, 1):
                z_after_block = run_block(z, digit, digit_index)
                if digit_index == 13:
                    if z_after_block == 0:
                        return digit
                else:
                    number = find_next(z_after_block, digit_index + 1)
                    if number is not None:
                        return digit * 10 ** (13 - digit_index) + number
            return None

        def run_block(z, w, digit_index):
            p1, p2, p3 = block_parameters[digit_index]
            _, x = divmod(z, 26)
            x += p2
            z = z // p1
            if x != w:
                z = 26 * z + w + p3
            return z

        return find_next(0, 0)

    def get_example_input(self, puzzle):
        return None


class PartB(PartA):
    def compute(self, data):
        return self.find_number(data.block_params, False)


Day.do_day(24, 2021, PartA, PartB)
