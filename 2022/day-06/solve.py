from mylib.aoc_basics import Day


class PartA(Day):
    def part_config(self, data):
        data.packet_length = 4

    def compute(self, data):
        for i in range(data.packet_length, len(data.text)):
            if PartA.all_different(data.text[i-data.packet_length:i]):
                return i

    @classmethod
    def all_different(cls, text):
        set_text = set(text)
        return len(set_text) == len(text)


class PartB(PartA):
    def part_config(self, data):
        data.packet_length = 14


Day.do_day(6, 2022, PartA, PartB)
