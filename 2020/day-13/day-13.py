import functools
import math
import operator
import re
from mylib.aoc_basics import Day


class PartA(Day):
    def parse(self, text, data):
        earliest_departure, bus_ids = text.splitlines()
        data.departure = int(earliest_departure)
        data.bus_ids = [int(x) for x in re.findall(r"\d+", bus_ids)]

    def compute(self, data):
        best_bus, wait_time = min(
            ((bus_id, self.wait_time(data.departure, bus_id)) for bus_id in data.bus_ids),
            key=lambda x: x[1],
        )
        return best_bus * wait_time

    @staticmethod
    def wait_time(current_time, bus_id):
        return bus_id - (current_time % bus_id)

    def example_answer(self):
        return 295


class PartB(Day):
    def parse(self, text, data):
        _, bus_ids = text.splitlines()
        bus_ids = bus_ids.split(",")
        data.bus_ids = [(int(bus_id), offset) for offset, bus_id in enumerate(bus_ids) if bus_id.isnumeric()]
        data.N = functools.reduce(operator.mul, (bus_id for bus_id, offset in data.bus_ids))

    def compute(self, data):
        result = 0
        for bus_id, offset in data.bus_ids:
            a = bus_id - offset % bus_id
            b = data.N // bus_id
            result += a * b * self.invmod(b, bus_id)
        return result % data.N

    def invmod(self, a, m):
        g, x, y = self.extended_euclid(a, m)
        return x % m

    @staticmethod
    def extended_euclid(x, y):
        x0, x1, y0, y1 = 1, 0, 0, 1
        while y > 0:
            q, x, y = math.floor(x / y), y, x % y
            x0, x1 = x1, x0 - q * x1
            y0, y1 = y1, y0 - q * y1
        return q, x0, y0

    def example_answer(self):
        return 1068781


Day.do_day(13, 2020, PartA, PartB)
