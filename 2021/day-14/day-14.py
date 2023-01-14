import functools
from collections import Counter
from mylib.aoc_basics import Day


class PartA(Day):
    def parse(self, text, data):
        data.template, rules_text = text.split("\n\n")
        data.rules = dict(line.split(" -> ") for line in rules_text.splitlines())
        data.steps = 10

    def compute(self, data):
        counter = self.run_steps(data)
        return max(counter.values()) - min(counter.values())

    @staticmethod
    def run_steps(data):
        @functools.cache
        def count(pair, step):
            if step == data.steps or pair not in data.rules:
                return Counter()

            step += 1
            insertion = data.rules[pair]
            counter = Counter(insertion)
            counter.update(count(pair[0] + insertion, step))
            counter.update(count(insertion + pair[1], step))
            return counter

        counter = Counter(data.template)
        for left, right in zip(data.template, data.template[1:]):
            counter.update(count(left + right, 0))
        return counter


class PartB(PartA):
    def part_config(self, data):
        data.steps = 40

    def example_answer(self):
        return 2188189693529


Day.do_day(14, 2021, PartA, PartB)
