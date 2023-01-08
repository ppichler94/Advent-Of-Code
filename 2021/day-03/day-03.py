from mylib.aoc_basics import Day


class PartA(Day):
    def parse(self, text, data):
        data.numbers = text.splitlines()

    def compute(self, data):
        gamma_rate = "".join(self.get_most_common_bit_at_pos(data.numbers, i) for i in range(len(data.numbers[0])))
        epsilon_rate = "".join({"0": "1", "1": "0"}.get(x) for x in gamma_rate)
        return int(gamma_rate, 2) * int(epsilon_rate, 2)

    @staticmethod
    def get_most_common_bit_at_pos(numbers, index):
        number_of_0s = sum(1 if number[index] == "0" else 0 for number in numbers)
        number_of_1s = sum(1 if number[index] == "1" else 0 for number in numbers)
        return "1" if number_of_1s >= number_of_0s else "0"

    def example_answer(self):
        return 198


class PartB(PartA):
    def compute(self, data):
        oxygen_numbers = self.filter(data.numbers, {"0": "0", "1": "1"})
        scrubber_numbers = self.filter(data.numbers, {"0": "1", "1": "0"})

        oxygen_rating = int(oxygen_numbers[0], 2)
        scrubber_rating = int(scrubber_numbers[0], 2)

        return oxygen_rating * scrubber_rating

    @classmethod
    def filter(cls, numbers, converter):
        for i in range(0, len(numbers[0])):
            bit = cls.get_most_common_bit_at_pos(numbers, i)
            numbers = list(filter(lambda number, i=i, bit=bit: number[i] == converter.get(bit), numbers))
            if len(numbers) == 1:
                break
        return numbers

    def example_answer(self):
        return 230


Day.do_day(3, 2021, PartA, PartB)
