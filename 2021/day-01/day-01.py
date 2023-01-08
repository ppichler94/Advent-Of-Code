from mylib.aoc_basics import Day


class PartA(Day):
    def parse(self, text, data):
        data.numbers = [int(x) for x in text.splitlines()]

    def compute(self, data):
        pairs = list(zip(data.numbers, data.numbers[1:]))
        return sum(1 if b > a else 0 for a, b in pairs)

    def example_answer(self):
        return 7


class PartB(PartA):
    def compute(self, data):
        sliding_window_generator = self.sliding_window(data.numbers, 3)
        window_sums = [sum(x) for x in sliding_window_generator]
        pairs = list(zip(window_sums, window_sums[1:]))
        return sum(1 if b > a else 0 for a, b in pairs)

    @staticmethod
    def sliding_window(elements, window_size):
        if len(elements) < window_size:
            return elements
        for i in range(len(elements) - window_size + 1):
            yield elements[i:i + window_size]

    def example_answer(self):
        return 5


Day.do_day(1, 2021, PartA, PartB)
