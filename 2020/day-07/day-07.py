import dataclasses
from typing import Dict
from mylib.aoc_basics import Day


@dataclasses.dataclass(frozen=True)
class Bag:
    name: str
    content: Dict[str, int]

    def contains(self, bags, bag):
        if bag in self.content.keys():
            return True
        for b in self.content.keys():
            if bags[b].contains(bags, bag):
                return True
        return False

    def content_count(self, bags):
        if self.content:
            return sum(count + count * bags[name].content_count(bags) for name, count in self.content.items())
        return 0

    @classmethod
    def from_string(cls, text):
        name, content_text = text.split(" bags contain ")
        bags_text = content_text.replace(".", "").split(", ")
        bags = [bag_text.replace(" bags", "").replace(" bag", "").split(" ") for bag_text in bags_text]
        content = dict() if "no" in bags_text[0] else {" ".join(bag): int(count) for count, *bag in bags}
        return cls(name, content)


class PartA(Day):
    def parse(self, text, data):
        bags = [Bag.from_string(line) for line in text.splitlines()]
        data.bags = {bag.name: bag for bag in bags}

    def compute(self, data):
        return sum(1 if bag.contains(data.bags, "shiny gold") else 0 for bag in data.bags.values())

    def example_answer(self):
        return 4


class PartB(PartA):
    def compute(self, data):
        return data.bags["shiny gold"].content_count(data.bags)

    def example_answer(self):
        return 32


Day.do_day(7, 2020, PartA, PartB)
