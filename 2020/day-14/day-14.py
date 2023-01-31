import re
from mylib.aoc_basics import Day


class PartA(Day):
    def parse(self, text, data):
        data.instructions = [self.parse_line(line) for line in text.splitlines()]

    @staticmethod
    def parse_line(line):
        if matcher := re.match(r"mask = (.*)", line):
            return "mask", matcher.group(1)
        if matcher := re.match(r"mem\[(\d+)\] = (\d+)", line):
            return "mem", int(matcher.group(1)), int(matcher.group(2))
        raise RuntimeError(f"Error parsing line {line}")

    def compute(self, data):
        mem = dict()
        current_mask = f"{0:036b}"
        for instruction in data.instructions:
            match instruction[0]:
                case "mask":
                    current_mask = instruction[1]
                case "mem":
                    mem[instruction[1]] = self.apply_mask(current_mask, instruction[2])
        return sum(mem.values())

    @staticmethod
    def apply_mask(mask, value):
        binary_value = f"{value:036b}"
        return int("".join(m if m != "X" else v for m, v in zip(mask, binary_value)), 2)

    def example_answer(self):
        return 165


class PartB(PartA):
    def compute(self, data):
        mem = dict()
        current_mask = f"{0:036b}"
        for instruction in data.instructions:
            match instruction[0]:
                case "mask":
                    current_mask = instruction[1]
                case "mem":
                    addresses = self.calculate_addresses(current_mask, instruction[1])
                    for address in addresses:
                        mem[address] = instruction[2]
        return sum(mem.values())

    def calculate_addresses(self, mask, address):
        binary_address = f"{address:036b}"
        masked_address = "".join(a if m == "0" else m for m, a in zip(mask, binary_address))
        addresses = [masked_address]
        floating = True
        while floating:
            new_addresses, floating = self.replace_floating(addresses.pop(0))
            addresses.extend(new_addresses)
        return addresses

    @staticmethod
    def replace_floating(address):
        floating_index = address.find("X")
        if floating_index == -1:
            return [address], False
        address1 = address.replace("X", "0", 1)
        address2 = address.replace("X", "1", 1)
        return [address1, address2], True

    def example_answer(self):
        return 208

    def get_example_input(self, puzzle):
        return """
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
"""


Day.do_day(14, 2020, PartA, PartB)
