def main():
    example_data = read_input_from_file("example.txt")
    input_data = read_input_from_file("input.txt")

    print(f'Result example A: {solve_a(example_data)}\n')
    print(f'Result puzzle data A: {solve_a(input_data)}\n')
    print(f'Result example B: {solve_b(example_data)}\n')
    print(f'Result puzzle data B: {solve_b(input_data)}\n')


def read_input_from_file(file_name):
    input_file = open(file_name, "r")
    data = input_file.readlines()
    input_file.close()
    data = [x.strip() for x in data]
    return data


class Monkey():
    def __init__(self, items, operation, test_number, true_destination, false_destination, worry_level_factor):
        self.items = items
        self.operation = operation
        self.test_number = test_number
        self.true_destination = true_destination
        self.false_destination = false_destination
        self.items_inspected = 0
        self.worry_level_factor = worry_level_factor

    def turn(self, monkeys):
        modulo = self.calculate_modulo(monkeys)
        for item in self.items:
            old = item
            exec(self.operation)
            item = locals()["new"]
            item //= self.worry_level_factor
            item %= modulo
            rest = item % self.test_number
            if rest == 0:
                monkeys[self.true_destination].add(item)
            else:
                monkeys[self.false_destination].add(item)
            self.items_inspected += 1
        self.items = []

    def calculate_modulo(self, monkeys):
        modulo = 1
        for monkey in monkeys:
            modulo *= monkey.test_number
        return modulo

    def add(self, item):
        self.items.append(item)

    @classmethod
    def from_string(cls, lines, worry_level_factor):
        items = [int(x) for x in lines[1].split(": ")[1].split(", ")]
        operation = lines[2].split(": ")[1]
        test_number = int(lines[3].split("by ")[1])
        true_destination = int(lines[4].split("monkey ")[1])
        false_destination = int(lines[5].split("monkey ")[1])
        return Monkey(items, operation, test_number, true_destination, false_destination, worry_level_factor)


def solve_a(input):
    monkeys = parse_input(input, 3)
    return solve(monkeys, 20)


def solve(monkeys, rounds):
    for _ in range(rounds):
        for monkey in monkeys:
            monkey.turn(monkeys)
    items_inspected = [monkey.items_inspected for monkey in monkeys]
    items_inspected.sort()
    return items_inspected[-1] * items_inspected[-2]


def parse_input(input, worry_level_factor):
    monkeys = []
    i = 0
    monkey_start = 0
    while i < len(input):
        if input[i] == "":
            monkeys.append(Monkey.from_string(input[monkey_start:i+1], worry_level_factor))
            monkey_start = i + 1
        i += 1
    monkeys.append(Monkey.from_string(input[monkey_start:i+1], worry_level_factor))
    return monkeys


def solve_b(input):
    monkeys = parse_input(input, 1)
    return solve(monkeys, 10000)


if __name__ == "__main__":
    main()
