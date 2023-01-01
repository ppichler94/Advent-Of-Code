from collections import deque

from mylib.aoc_basics import Day


class PartA(Day):
    def parse(self, text, data):
        ints = [int(x) for x in text.splitlines()]
        data.zero_index = ints.index(0)
        data.numbers_orig = list(enumerate(ints))
        data.numbers = deque(data.numbers_orig)

    def compute(self, data):
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
            data.numbers.rotate(-number)


    def example_answer(self):
        return 3


class PartB(Day):
    pass


Day.do_day(20, 2022, PartA, PartB)
