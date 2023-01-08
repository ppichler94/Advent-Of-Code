from mylib.aoc_basics import Day


class PartA(Day):
    def parse(self, text, data):
        def run(lines):
            x = 1
            for line in lines:
                match line.split():
                    case ["noop"]:
                        yield x
                    case ["addx", parameter_text]:
                        yield x
                        yield x
                        x += int(parameter_text)
        data.generator = run(text.splitlines())

    def compute(self, data):
        result = 0
        interesting_cycles = {20, 60, 100, 140, 180, 220}
        for cycle, x in enumerate(data.generator, 1):
            if cycle in interesting_cycles:
                result += cycle * x
        return result

    def example_answer(self):
        return 13140

    def get_example_input(self, puzzle):
        return """
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
"""


class PartB(PartA):
    def compute(self, data):
        for _ in range(6):
            for column in range(40):
                x = next(data.generator)
                print("#" if x-1 <= column <= x+1 else ".", end="")
            print()

    def example_answer(self):
        return None


Day.do_day(10, 2022, PartA, PartB)

