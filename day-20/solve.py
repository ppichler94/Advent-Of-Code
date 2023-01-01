from collections import deque
from mylib.aoc_basics import Day


class PartA(Day):
    def parse(self, text, data):
        data.raw_numbers = [int(x) for x in text.splitlines()]
        data.zero_index = data.raw_numbers.index(0)

    def part_config(self, data):
        data.key = 1
        data.rounds = 1

    def compute(self, data):
        data.numbers_orig = list(enumerate(x * data.key for x in data.raw_numbers))
        data.numbers = deque(data.numbers_orig)

        for _ in range(data.rounds):
            self.mix(data)

        zero_index = data.numbers.index((data.zero_index, 0))
        number1 = data.numbers[(zero_index + 1000) % len(data.numbers)][1]
        number2 = data.numbers[(zero_index + 2000) % len(data.numbers)][1]
        number3 = data.numbers[(zero_index + 3000) % len(data.numbers)][1]
        return number1 + number2 + number3

    def mix(self, data):
        for id, number in data.numbers_orig:
            index = data.numbers.index((id, number))
            data.numbers.rotate(-index)
            data.numbers.popleft()
            data.numbers.rotate(-number)
            data.numbers.appendleft((id, number))

    def example_answer(self):
        return 3


class PartB(PartA):
    def part_config(self, data):
        data.key = 811589153
        data.rounds = 10

    def example_answer(self):
        return 1623178306


Day.do_day(20, 2022, PartA, PartB)
