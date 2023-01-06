from mylib.aoc_basics import Day

snafu_for_int = dict(enumerate("=-012", -2))
int_for_snafu = dict(map(reversed, snafu_for_int.items()))


def snafu_to_int(text):
    return sum(int_for_snafu[x] * 5**i for i, x in enumerate(text[::-1]))


def int_to_snafu(number):
    if not number:
        return ""

    result = ""
    while number != 0:
        new_number, rest = divmod(number, 5)
        if rest > 2:
            rest -= 5
            new_number += 1
        result += snafu_for_int[rest]
        number = new_number

    return result[::-1]


class PartA(Day):
    def compute(self, data):
        result = 0
        for number_text in data.text.splitlines():
            result += snafu_to_int(number_text)

        return int_to_snafu(result)

    def example_answer(self):
        return "2=-1=0"


Day.do_day(25, 2022, PartA, None)
