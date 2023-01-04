from collections import Counter
from functools import lru_cache


def read_input_from_file(file_name):
    input_file = open(file_name, "r")
    input = input_file.readlines()
    input = [x.strip() for x in input]
    input_file.close()
    return input


def parse_input(input):
    template = input[0]
    rules = {}
    for line in input[2:]:
        s = line.split(" -> ")
        rules[s[0]] = s[1]
    return [template, rules]


def run_steps(template, rules, step_count):
    @lru_cache(maxsize=None)
    def count(pair, step):
        if step == step_count or pair not in rules:
            return Counter()

        step += 1
        insertion = rules[pair]
        counter = Counter(insertion)
        counter.update(count(pair[0] + insertion, step))
        counter.update(count(insertion + pair[1], step))
        return counter

    counter = Counter(template)
    for left, right in zip(template, template[1:]):
        counter.update(count(left + right, 0))
    return counter


def run(input, steps):
    [template, rules] = parse_input(input)
    counter = run_steps(template, rules, steps)
    maximum = max(counter.values())
    minimum = min(counter.values())
    return maximum - minimum


def main():
    example = read_input_from_file("day-14/example.txt")
    input = read_input_from_file("day-14/input.txt")

    print(f'Result example A: {run(example, 10)}\n')
    print(f'Result puzzle data A: {run(input, 10)}\n')
    print(f'Result example B: {run(example, 40)}\n')
    print(f'Result puzzle data B: {run(input, 40)}\n')


if __name__ == "__main__":
    main()
