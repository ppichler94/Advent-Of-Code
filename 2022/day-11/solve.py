from mylib.aoc_basics import Day


class Monkey:
    def __init__(self, items, operation, test_number, true_destination, false_destination):
        self.items = items
        self.operation = operation
        self.test_number = test_number
        self.true_destination = true_destination
        self.false_destination = false_destination
        self.items_inspected = 0

    def turn(self, monkeys, worry_level_factor):
        modulo = Monkey.calculate_modulo(monkeys)
        for item in self.items:
            old = item
            exec(self.operation)
            item = locals()["new"]
            item //= worry_level_factor
            item %= modulo
            rest = item % self.test_number
            if rest == 0:
                monkeys[self.true_destination].add(item)
            else:
                monkeys[self.false_destination].add(item)
            self.items_inspected += 1
        self.items = []

    @staticmethod
    def calculate_modulo(monkeys):
        modulo = 1
        for monkey in monkeys:
            modulo *= monkey.test_number
        return modulo

    def add(self, item):
        self.items.append(item)

    @staticmethod
    def from_string(lines):
        items = [int(x) for x in lines[1].split(": ")[1].split(", ")]
        operation = lines[2].split(": ")[1]
        test_number = int(lines[3].split("by ")[1])
        true_destination = int(lines[4].split("monkey ")[1])
        false_destination = int(lines[5].split("monkey ")[1])
        return Monkey(items, operation, test_number, true_destination, false_destination)


class PartA(Day):
    def parse(self, text, data):
        data.monkeys = []
        for block in text.split("\n\n"):
            data.monkeys.append(Monkey.from_string(block.splitlines()))

    def part_config(self, data):
        data.rounds = 20
        data.worry_level_factor = 3

    def compute(self, data):
        for _ in range(data.rounds):
            for monkey in data.monkeys:
                monkey.turn(data.monkeys, data.worry_level_factor)
        items_inspected = [monkey.items_inspected for monkey in data.monkeys]
        items_inspected.sort()
        return items_inspected[-1] * items_inspected[-2]

    def example_answer(self):
        return 10605


class PartB(PartA):
    def part_config(self, data):
        data.rounds = 10000
        data.worry_level_factor = 1

    def example_answer(self):
        return 2713310158


Day.do_day(11, 2022, PartA, PartB)
