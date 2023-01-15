import math
import re
import itertools
from mylib.aoc_basics import Day


class PartA(Day):
    def parse(self, text, data):
        data.numbers = text.splitlines()

    def compute(self, data):
        number = data.numbers.pop(0)
        while len(data.numbers) > 0:
            next_number = data.numbers.pop(0)
            number = f"[{number},{next_number}]"
            number = self.reduce(number)
        return self.magnitude(number)

    @staticmethod
    def explode(data):
        offset = 0
        for number in re.findall(r"\[\d+,\d+]", data):
            pair = re.search(re.escape(number), data[offset:])
            num_left_brackets = data[:pair.start() + offset].count("[")
            num_right_brackets = data[:pair.start() + offset].count("]")
            if num_left_brackets - num_right_brackets >= 4:
                left, right = pair.group()[1:-1].split(",")
                left_part = data[:pair.start() + offset][::-1]
                right_part = data[pair.end() + offset:]
                search_left = re.search(r"\d+", left_part)
                if search_left:
                    x = int(left_part[search_left.start():search_left.end()][::-1]) + int(left)
                    left_part = f"{left_part[:search_left.start()]}{str(x)[::-1]}{left_part[search_left.end():]}"
                search_right = re.search(r"\d+", right_part)
                if search_right:
                    x = int(right_part[search_right.start():search_right.end()]) + int(right)
                    right_part = f"{right_part[:search_right.start()]}{str(x)}{right_part[search_right.end():]}"
                data = f"{left_part[::-1]}0{right_part}"
                break
            else:
                offset += pair.end()

        return data

    @staticmethod
    def split(data):
        number = re.search(r"\d\d", data)
        if number:
            left_part = data[:number.start()]
            right_part = data[number.end():]
            new_left_digit = int(math.floor(int(number.group()) / 2))
            new_right_digit = int(math.ceil(int(number.group()) / 2))
            data = f"{left_part}[{new_left_digit},{new_right_digit}]{right_part}"
        return data

    def reduce(self, data):
        exploded = self.explode(data)
        if exploded != data:
            return self.reduce(exploded)
        else:
            splitted = self.split(data)
            if splitted != data:
                return self.reduce(splitted)
        return splitted

    @staticmethod
    def magnitude(data):
        while data.count(",") > 1:
            for number in re.findall(r"\[\d+,\d+\]", data):
                pair = re.search(re.escape(number), data)
                left_digit, right_digit = number[1:-1].split(",")
                data = f"{data[:pair.start()]}{int(left_digit) * 3 + int(right_digit) * 2}{data[pair.end():]}"
        left_digit, right_digit = data[1:-1].split(",")
        return int(left_digit) * 3 + int(right_digit) * 2

    def example_answer(self):
        return 4230


class PartB(PartA):
    def compute(self, data):
        pairs = list(itertools.permutations(data.numbers, 2))
        return max(self.magnitude_of_pair(pair) for pair in pairs)

    def magnitude_of_pair(self, pair):
        number = f"[{pair[0]},{pair[1]}]"
        number = self.reduce(number)
        return self.magnitude(number)

    def example_answer(self):
        return 4647


Day.do_day(18, 2021, PartA, PartB)
