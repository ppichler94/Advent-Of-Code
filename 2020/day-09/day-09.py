import itertools
from mylib.aoc_basics import Day


class PartA(Day):
    def parse(self, text, data):
        data.numbers = [int(x) for x in text.splitlines()]
        data.preamble_size = 5 if data.config is not None else 25

    def compute(self, data):
        return self.find_invalid_number(data.numbers, data.preamble_size)

    @staticmethod
    def find_invalid_number(numbers, preamble_size):
        for i in range(preamble_size, len(numbers)):
            if numbers[i] not in [sum(x) for x in itertools.combinations(numbers[i - preamble_size : i], 2)]:
                return numbers[i]

    def example_answer(self):
        return 127


class PartB(PartA):
    def compute(self, data):
        invalid_number = self.find_invalid_number(data.numbers, data.preamble_size)
        for window in itertools.chain.from_iterable(
            self.sliding_window(data.numbers, size) for size in range(2, len(data.numbers))
        ):
            if sum(window) == invalid_number:
                return min(window) + max(window)

    @staticmethod
    def sliding_window(elements, window_size):
        if len(elements) < window_size:
            return elements
        for i in range(len(elements) - window_size + 1):
            yield elements[i : i + window_size]

    def example_answer(self):
        return 62


Day.do_day(9, 2020, PartA, PartB)
