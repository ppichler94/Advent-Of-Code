from functools import cache
from mylib.aoc_basics import Day


class PartA(Day):
    def parse(self, text, data):
        data.orbits = {k: v for v, k in [line.split(")") for line in text.splitlines()]}

    def compute(self, data):
        @cache
        def count_orbits(obj):
            if obj == "COM":
                return 0
            return 1 + count_orbits(data.orbits[obj])

        return sum(count_orbits(obj) for obj in data.orbits.keys())

    def example_answer(self):
        return 42

    def get_example_input(self, puzzle):
        return "COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L"


class PartB(PartA):
    def compute(self, data):
        counts_you = self.count_orbits(data, "YOU")
        counts_santa = self.count_orbits(data, "SAN")
        orbit_sums = {
            obj: counts_santa[obj] + counts_you[obj]
            for obj in data.orbits.keys()
            if obj in counts_you and obj in counts_santa
        }
        return min(orbit_sums.values())

    @staticmethod
    def count_orbits(data, start):
        current = start
        counts = dict()
        count = -1
        while current != "COM":
            counts[current] = count
            count += 1
            current = data.orbits[current]
        return counts

    def example_answer(self):
        return 4

    def get_example_input(self, puzzle):
        return "COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L\nK)YOU\nI)SAN"


Day.do_day(6, 2019, PartA, PartB)
