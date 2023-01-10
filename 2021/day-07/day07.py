import numpy as np
from mylib.aoc_basics import Day


class PartA(Day):
    def parse(self, text, data):
        data.positions = np.array(text.split(","), dtype=int)

    def part_config(self, data):
        def cost_function(positions, target):
            return np.absolute(positions - target).sum()

        data.cost_function = cost_function

    def compute(self, data):
        minimal_cost = self.calculate_fuel_usage(data)
        return minimal_cost

    @staticmethod
    def calculate_fuel_usage(data):
        min_value = data.positions.min()
        max_value = data.positions.max()
        minimal_cost = data.cost_function(data.positions, min_value)
        for target in range(min_value, max_value):
            cost = data.cost_function(data.positions, target)
            if cost < minimal_cost:
                minimal_cost = cost

        return int(minimal_cost)

    def example_answer(self):
        return 37


class PartB(PartA):
    def part_config(self, data):
        def cost_function(positions, target):
            distance = np.absolute(positions - target)
            return (distance * (distance + 1) * 0.5).sum()

        data.cost_function = cost_function

    def example_answer(self):
        return 168


Day.do_day(7, 2021, PartA, PartB)
