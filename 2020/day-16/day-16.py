import dataclasses
import operator
from functools import partial, reduce
from typing import Tuple
from mylib.aoc_basics import Day


@dataclasses.dataclass
class Validator:
    name: str
    range1: Tuple[int, int]
    range2: Tuple[int, int]

    def validate(self, number):
        return self.range1[0] <= number <= self.range1[1] or self.range2[0] <= number <= self.range2[1]

    @classmethod
    def from_string(cls, text):
        name, ranges = text.split(": ")
        range1_text, range2_text = ranges.split(" or ")
        range1 = tuple(int(x) for x in range1_text.split("-"))
        range2 = tuple(int(x) for x in range2_text.split("-"))
        return cls(name, range1, range2)


class PartA(Day):
    def parse(self, text, data):
        validators, my_ticket, other_tickets = text.split("\n\n")
        data.validators = [Validator.from_string(line) for line in validators.splitlines()]
        data.my_ticket = [int(x) for x in my_ticket.splitlines()[1].split(",")]
        data.tickets = [[int(x) for x in line.split(",")] for line in other_tickets.splitlines()[1:]]

    def compute(self, data):
        return sum(self.sum_invalid_values(data.validators, ticket) for ticket in data.tickets)

    @staticmethod
    def sum_invalid_values(validators, ticket):
        return sum(0 if any(validator.validate(number) for validator in validators) else number for number in ticket)

    def example_answer(self):
        return 71

    def get_example_input(self, puzzle):
        return """
class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
"""


class PartB(PartA):
    def compute(self, data):
        valid_tickets = list(filter(partial(self.validate_ticket, data.validators), data.tickets))
        possible_assignments = dict()
        for validator in data.validators:
            possible_assignments[validator.name] = set()
            for i in range(len(data.tickets[0])):
                if all(validator.validate(number) for number in [ticket[i] for ticket in valid_tickets]):
                    possible_assignments[validator.name].add(i)

        assignments = dict()
        while len(possible_assignments) > 0:
            assignment = [(name, indices) for name, indices in possible_assignments.items() if len(indices) == 1][0]
            index = assignment[1].pop()
            assignments[assignment[0]] = index
            for _, indices in possible_assignments.items():
                indices.discard(index)
            possible_assignments.pop(assignment[0])

        departure_indices = [i for name, i in assignments.items() if "departure" in name]
        return reduce(operator.mul, (data.my_ticket[i] for i in departure_indices))

    @staticmethod
    def validate_ticket(validators, ticket):
        return all(any(validator.validate(number) for validator in validators) for number in ticket)

    def get_example_input(self, puzzle):
        return None


Day.do_day(16, 2020, PartA, PartB)
