import operator
from mylib.aoc_basics import Day


class PartA(Day):
    def parse(self, text, data):
        adapters = list(sorted(int(x) for x in text.splitlines()))
        data.adapters = [0] + adapters + [adapters[-1] + 3]

    def compute(self, data):
        diff = list(map(operator.sub, data.adapters[1:], data.adapters))
        return diff.count(1) * diff.count(3)

    def example_answer(self):
        return 7 * 5


class PartB(PartA):
    def compute(self, data):
        possibilities = 1
        diff = map(operator.sub, data.adapters[2:], data.adapters)
        optionals = list(map(lambda x: x <= 3, diff))
        for i in range(len(optionals)):
            if i > 1 and optionals[i - 2] == optionals[i - 1] == optionals[i] == True:
                possibilities *= 1.75
            elif optionals[i]:
                possibilities *= 2
        return int(possibilities)

    def example_answer(self):
        return 8

    def tests(self):
        yield "28\n33\n18\n42\n31\n14\n46\n20\n48\n47\n24\n23\n49\n45\n19\n38\n39\n11\n1\n32\n25\n35\n8\n17\n7\n9\n4\n2\n34\n10\n3", 19208, "Larger example"


Day.do_day(10, 2020, PartA, PartB)
