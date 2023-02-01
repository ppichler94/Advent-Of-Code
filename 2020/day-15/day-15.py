from mylib.aoc_basics import Day


class PartA(Day):
    def parse(self, text, data):
        data.numbers = [int(x) for x in text.split(",")]
        data.target_turn = 2020

    def compute(self, data):
        already_seen = dict()
        for turn, number in enumerate(data.numbers, 1):
            self.set_already_seen(already_seen, number, turn)

        next_number = data.numbers[-1]
        for turn in range(len(data.numbers) + 1, data.target_turn):
            next_number = self.get_next_number(already_seen, next_number)
            self.set_already_seen(already_seen, next_number, turn)

        return self.get_next_number(already_seen, next_number)

    @staticmethod
    def set_already_seen(already_seen, number, turn):
        if number in already_seen:
            turns = already_seen[number]
            turns[1] = turns[0]
            turns[0] = turn
        else:
            already_seen[number] = [turn, 0]

    @staticmethod
    def get_next_number(already_seen, last_number):
        return 0 if not already_seen[last_number][1] else already_seen[last_number][0] - already_seen[last_number][1]

    def get_example_input(self, puzzle):
        return None

    def tests(self):
        yield "1,3,2", 1, "Test1"
        yield "2,1,3", 10, "Test2"
        yield "1,2,3", 27, "Test3"
        yield "2,3,1", 78, "Test4"
        yield "3,2,1", 438, "Test5"
        yield "3,1,2", 1836, "Test6"


class PartB(PartA):
    def part_config(self, data):
        data.target_turn = 30000000

    def tests(self):
        yield "1,3,2", 2578, "Test1"
        yield "2,1,3", 3544142, "Test2"


Day.do_day(15, 2020, PartA, PartB)
