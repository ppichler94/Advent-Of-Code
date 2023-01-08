from mylib.aoc_basics import Day


class PartA(Day):
    def parse(self, text, data):
        data.instructions = [(command, int(count))
                             for command, count
                             in [s.split(" ") for s in text.splitlines()]]

    def compute(self, data):
        horizontal_pos = 0
        depth = 0

        for instruction in data.instructions:
            match instruction:
                case ("forward", count):
                    horizontal_pos += count
                case ("down", count):
                    depth += count
                case ("up", count):
                    depth -= count

        return horizontal_pos * depth

    def example_answer(self):
        return 150


class PartB(PartA):
    def compute(self, data):
        horizontal_pos = 0
        depth = 0
        aim = 0

        for instruction in data.instructions:
            match instruction:
                case ("forward", count):
                    horizontal_pos += count
                    depth += aim * count
                case ("down", count):
                    aim += count
                case ("up", count):
                    aim -= count

        return horizontal_pos * depth

    def example_answer(self):
        return 900


Day.do_day(2, 2021, PartA, PartB)
