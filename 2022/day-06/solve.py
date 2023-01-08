from mylib.aoc_basics import Day


class PartA(Day):
    def part_config(self, data):
        data.packet_length = 4

    def compute(self, data):
        for i in range(data.packet_length, len(data.text)):
            if PartA.all_different(data.text[i-data.packet_length:i]):
                return i

    @staticmethod
    def all_different(text):
        set_text = set(text)
        return len(set_text) == len(text)

    def example_answer(self):
        return 7

    def tests(self):
        yield "bvwbjplbgvbhsrlpgdmjqwftvncz", 5, "Example2"
        yield "nppdvjthqldpwncqszvftbrmjlhg", 6, "Example3"
        yield "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 10, "Example4"
        yield "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 11, "Example5"


class PartB(PartA):
    def part_config(self, data):
        data.packet_length = 14

    def example_answer(self):
        return 19

    def tests(self):
        yield "bvwbjplbgvbhsrlpgdmjqwftvncz", 23, "Example2"
        yield "nppdvjthqldpwncqszvftbrmjlhg", 23, "Example3"
        yield "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 29, "Example4"
        yield "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 26, "Example5"


Day.do_day(6, 2022, PartA, PartB)
