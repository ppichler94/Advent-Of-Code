import sys
import timeit
from aocd.models import Puzzle


def submit(puzzle: Puzzle, answer, value):
    print()
    print("  >>", answer, ": ", value)
    if answer not in ("answer_a", "answer_b"):
        print("Answer ignored: answer does not match answer_a or answer_b")
        return

    if type(value) == int:
        value_str = str(value)
    elif type(value) == str:
        value_str = value
    else:
        print("Answer ignored: value type is neither int nor string")
        return

    if answer == "answer_a" and puzzle.answered_a:
        if value_str == puzzle.answer_a:
            print("  >> Ok (Already answered, values match)")
        else:
            print("  >> Value differs from previous: ", puzzle.answer_a)
        return


    if answer == "answer_b" and puzzle.answered_b:
        if value_str == puzzle.answer_b:
            print("  >> Ok (Already answered, values match)")
        else:
            print("  >> Value differs from previous: ", puzzle.answer_b)
        return

    print("Submit answer? (y/n)")
    f = sys.stdin
    line = f.read(1)
    if line == "y":
        setattr(puzzle, answer, value_str)
        print("Answer Submitted")


class Something:
    pass


class Day:
    def answer_name(self):
        part = type(self).__name__[:5]
        if part not in ("PartA", "PartB"):
            raise RuntimeError("Class name must start with PartA or PartB")
        return "answer_" + part[-1].lower()

    def parse(self, text, data):
        data.text = text

    def part_config(self, data):
        pass

    def compute(self, data):
        return ''

    def tests(self):
        return []

    def test_solve(self, test_text, config=None):
        data = Something()
        data.config = config
        print("Parse input")
        self.parse(test_text.strip("\n"), data)
        print("Config")
        self.part_config(data)
        print("Compute")
        result = self.compute(data)
        return result

    def test(self):
        print("Starting test...")
        t = timeit.default_timer()
        all_ok = True
        for result, result_ok, *more in self.tests():
            test_name = "" if len(more) == 0 else f"'{more[0]}'"
            if result == result_ok:
                print(f"  >> Test {test_name} OK  Result: {result}")
            else:
                print(f"  >> Test {test_name} Failed")
                print(f"  !! Expected {result_ok} but got {result}")
                all_ok = False
        print(f"Testing finished after {timeit.default_timer() - t:.2f}s")
        print("")
        return all_ok

    def do_solve(self, puzzle_text):
        print("Starting to solve...")
        t = timeit.default_timer()
        data = Something()
        data.config = None
        print("Parse input")
        self.parse(puzzle_text, data)
        print("Config")
        self.part_config(data)
        print("Compute")
        result = self.compute(data)
        print(f"Finished solving after {timeit.default_timer() - t:.2f}s")
        return result

    def do_part(self, puzzle):
        print(f"-------------------- starting {self.answer_name()} --------------------")
        if self.test():
            text = puzzle.input_data
            result = self.do_solve(text)
            submit(puzzle, self.answer_name(), result)
        print()

    @staticmethod
    def do_day(day, year, part_a, part_b):
        puzzle = Puzzle(day=day, year=year)
        part_a().do_part(puzzle)
        part_b().do_part(puzzle)
