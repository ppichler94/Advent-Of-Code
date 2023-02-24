from mylib.aoc_basics import Day


class PartA(Day):
    def parse(self, text, data):
        data.masses = [int(line) for line in text.splitlines()]

    def compute(self, data):
        return sum(self.fuel_required(mass) for mass in data.masses)

    def fuel_required(self, mass):
        return mass // 3 - 2

    def tests(self):
        yield "12", 2, "Example1",
        yield "14", 2, "Example2",
        yield "1969", 654, "Example3",
        yield "12\n1969\n100756", 34239, "Multiple lines"


class PartB(PartA):
    def fuel_required(self, mass):
        fuel = mass // 3 - 2
        total_fuel = fuel
        while fuel := max(0, fuel // 3 - 2):
            total_fuel += fuel
        return total_fuel

    def tests(self):
        yield "14", 2, "Example1",
        yield "1969", 966, "Example2",
        yield "14\n1969\n100756", 51314, "Multiple lines"


Day.do_day(1, 2019, PartA, PartB)
