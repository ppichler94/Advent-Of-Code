import dataclasses
import re
from itertools import chain
from typing import List
from mylib.aoc_basics import Day
import pyparsing


class Group:
    def match(self, rules, text) -> List[str]:
        ...


@dataclasses.dataclass
class LiteralGroup(Group):
    value: str

    def __init__(self, tokens):
        self.value = tokens[0]

    def match(self, rules, text):
        if text and text[0] == self.value:
            return [text[1:]]
        else:
            return []


@dataclasses.dataclass
class AndGroup(Group):
    numbers: List[str]

    def __init__(self, tokens):
        self.numbers = list(tokens)

    def match(self, rules, text):
        previous_matches = [text]
        for number in self.numbers:
            previous_matches = list(chain.from_iterable(rules[number].match(rules, t) for t in previous_matches))
            if len(previous_matches) == 0:
                return []
        return previous_matches


@dataclasses.dataclass
class OrGroup(Group):
    and_groups: List[Group]

    def __init__(self, tokens):
        self.and_groups = list(tokens)

    def match(self, rules, text):
        matches = []
        for group in self.and_groups:
            matches.extend(group.match(rules, text))
        return matches


@dataclasses.dataclass
class Rule:
    name: str
    group: Group

    def __init__(self, tokens):
        self.name = tokens[0]
        self.group = tokens[1]

    def match(self, rules, text):
        matches = self.group.match(rules, text)
        return matches


class PartA(Day):
    def parse(self, text, data):
        rule_text, message_text = text.split("\n\n")
        data.rules = rule_text.splitlines()
        data.messages = message_text.splitlines()

    def part_config(self, data):
        pyparsing.ParserElement.enable_packrat()
        number = pyparsing.Word(pyparsing.nums)
        literal = pyparsing.Suppress('"') + pyparsing.Word(pyparsing.alphas) + pyparsing.Suppress('"')
        and_group = number[1, ...]
        or_group = and_group + (pyparsing.Suppress("|") + and_group)[...]
        rule = number + pyparsing.Suppress(":") + (literal | or_group)

        literal.setParseAction(LiteralGroup)
        and_group.setParseAction(AndGroup)
        or_group.setParseAction(OrGroup)
        rule.setParseAction(Rule)

        rules = [rule.parseString(line)[0] for line in data.rules]
        data.rules2 = {rule.name: rule for rule in rules}
        data.rule_matcher = data.rules2["0"]

    def compute(self, data):
        return sum(1 if self.check_message(data.rule_matcher, data.rules2, line) else 0 for line in data.messages)

    @staticmethod
    def check_message(matcher, rules, message):
        match = matcher.match(rules, message)
        return match is not None and any(len(m) == 0 for m in match)

    def example_answer(self):
        return 2

    def get_example_input(self, puzzle):
        return """
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
"""


class PartB(PartA):
    def part_config(self, data):
        rule8_index = next(i for i, line in enumerate(data.rules) if re.match(r"^8: ", line))
        rule11_index = next(i for i, line in enumerate(data.rules) if re.match(r"^11: ", line))
        data.rules[rule8_index] = "8: 42 | 42 8"
        data.rules[rule11_index] = "11: 42 31 | 42 11 31"
        super(PartB, self).part_config(data)

    def example_answer(self):
        return 12

    def get_example_input(self, puzzle):
        return """
42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
"""


Day.do_day(19, 2020, PartA, PartB)
