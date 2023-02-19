import sys
import timeit
from aocd.models import Puzzle
from rich import print
from rich.console import Console
from rich.progress import Progress


def submit(puzzle: Puzzle, answer: str, value):
    def print_result(result):
        if result:
            print(f"  >> [green](Already answered, values match)[/green]")
        else:
            print(f"  >> [red]Value differs from previous:[/red] ", puzzle.answer_b)

    if answer not in ("answer_a", "answer_b"):
        print(f":warning: [yellow]Answer ignored:[/yellow] answer does not match answer_a or answer_b")
        return

    if type(value) == int:
        value_str = str(value)
    elif type(value) == str:
        value_str = value
    else:
        print(f":warning: [yellow]Answer ignored:[/yellow] value type is neither int nor string")
        return

    if answer == "answer_a" and puzzle.answered_a:
        print_result(value_str == puzzle.answer_a)
        return

    if answer == "answer_b" and puzzle.answered_b:
        print_result(value_str == puzzle.answer_b)
        return

    print("Submit answer? (y/n)")
    f = sys.stdin
    line = f.read(1)
    if line[0] == "y":
        setattr(puzzle, answer, value_str)
        print("Answer Submitted")


class Something:
    pass


class Day:
    def __answer_name(self):
        part = type(self).__name__[:5]
        if part not in ("PartA", "PartB"):
            raise RuntimeError("Class name must start with PartA or PartB")
        return "answer_" + part[-1].lower()

    def parse(self, text, data):
        data.text = text

    def part_config(self, data):
        # Optional configuration which differs between part a and part b
        pass

    def compute(self, data):
        raise NotImplementedError()

    def tests(self):
        return []

    def __test(self, puzzle: Puzzle):
        print("Starting test...")
        tests = self.__get_all_tests(puzzle)
        test_tasks = [Task(self, more[0], text.strip("\n"), target, more[1:]) for text, target, *more in tests]
        with Progress() as progress:
            task = progress.add_task("Tests...", total=len(tests))
            for test in test_tasks:
                test.execute()
                progress.update(task, advance=1)
            passed_tests = sum(1 if task.passed else 0 for task in test_tasks)
            runtime = sum(task.t for task in test_tasks)
            print(f"Testing finished after {runtime:.2f}s")
            print(f"{passed_tests} of {len(tests)} passed")
        print("")
        return passed_tests == len(tests)

    def __get_all_tests(self, puzzle: Puzzle):
        if self.get_example_input(puzzle):
            tests = [(self.get_example_input(puzzle), self.example_answer(), "Example", "example run")]
        else:
            tests = []
        tests.extend(self.tests())
        return tests

    def do_part(self, puzzle: Puzzle):
        console = Console()
        console.rule(f"starting {self.__answer_name()}")
        test_successful = self.__test(puzzle)
        if test_successful:
            text = puzzle.input_data
            task = Task(self, "Answer", text, None, None)
            task.execute()
            submit(puzzle, self.__answer_name(), task.result)
        print()

    def example_answer(self):
        return None

    def get_example_input(self, puzzle):
        return puzzle.example_data

    @classmethod
    def do_day(cls, day, year, part_a, part_b):
        puzzle = Puzzle(day=day, year=year)
        if part_a:
            part_a().do_part(puzzle)
        if part_b:
            part_b().do_part(puzzle)


class Task:
    def __init__(self, day: Day, name, input_text, target_result, config):
        self.day = day
        self.name = name
        self.input_text = input_text
        self.target_result = target_result
        self.config = config
        self.result = None
        self.passed = False

    def execute(self):
        self.__solve()
        if self.target_result is None:
            print(f"  [yellow]>>[/yellow] Task '{self.name}' [yellow bold]unchecked[/yellow bold]  Result: {self.result} Runtime: {self.t:.2f}s")
            self.passed = True
        elif self.result == self.target_result:
            print(f"  [green]>>[/green] Task '{self.name}' [green bold]OK[/green bold]  Result: {self.result} Runtime: {self.t:.2f}s")
            self.passed = True
        else:
            print(f"  [red]>>[/red]  Task '{self.name}' [red bold]failed[/red bold] Result: {self.result} Expected: {self.target_result} Runtime: {self.t:.2f}s")
            self.passed = False

    def __solve(self):
        t = timeit.default_timer()
        data = Something()
        data.config = self.config
        self.day.parse(self.input_text, data)
        self.day.part_config(data)
        self.result = self.day.compute(data)
        self.t = timeit.default_timer() - t
