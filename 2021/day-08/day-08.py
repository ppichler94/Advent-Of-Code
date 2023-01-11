from mylib.aoc_basics import Day


class PartA(Day):
    def parse(self, text, data):
        data.lines = [[part.split(" ") for part in line.split(" | ")] for line in text.splitlines()]

    def compute(self, data):
        return sum(1 if len(value) in [2, 3, 4, 7] else 0 for line in data.lines for value in line[1])

    def example_answer(self):
        return 26

    def get_example_input(self, puzzle):
        return """
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
"""


class PartB(PartA):
    def compute(self, data):
        total = 0

        for signal_pattern, output_value in data.lines:
            signal_pattern = [''.join(sorted(w)) for w in signal_pattern]
            output_value = [''.join(sorted(w)) for w in output_value]
            tmp = {}
            self.find_uniques(signal_pattern, tmp)
            self.find6(signal_pattern, tmp)
            self.find0(signal_pattern, tmp)
            self.find9(signal_pattern, tmp)
            self.find5(signal_pattern, tmp)
            self.find3(signal_pattern, tmp)
            self.find2(signal_pattern, tmp)

            code = {v: k for k, v in tmp.items()}
            total += int(''.join([code[word] for word in output_value]))
        return total

    @staticmethod
    def find_uniques(line, tmp):
        length_map = {2: "1", 3: "7", 4: "4", 7: "8"}
        for word in line:
            if len(word) in length_map:
                tmp[length_map[len(word)]] = word

    # one character is different between 1 and 6
    @staticmethod
    def find6(line, tmp):
        for word in line:
            if len(word) == 6 and any(character not in word for character in tmp["1"]):
                tmp["6"] = word
                break

    # one character is different between 0 and 4. Also one character difference to 6 (so find 6 first)
    @staticmethod
    def find0(line, tmp):
        for word in line:
            if (len(word) == 6
                    and any(character not in word for character in tmp["4"])
                    and word not in tmp.values()):
                tmp["0"] = word
                break

    # only 6 character number left after finding 0 and 6
    @staticmethod
    def find9(line, tmp):
        for word in line:
            if len(word) == 6 and word not in tmp.values():
                tmp["9"] = word
                break

    # all characters of 5 are in 6
    @staticmethod
    def find5(line, tmp):
        for word in line:
            if len(word) == 5 and all(character in tmp["6"] for character in word):
                tmp["5"] = word
                break

    # all characters of 3 are in 9 and 5 (find 5 first)
    @staticmethod
    def find3(line, tmp):
        for word in line:
            if (len(word) == 5
                    and all(character in tmp["9"] for character in word)
                    and word not in tmp.values()):
                tmp["3"] = word
                break

    # only 5 character number left after finding 5 and 3
    @staticmethod
    def find2(line, tmp):
        for word in line:
            if len(word) == 5 and word not in tmp.values():
                tmp["2"] = word
                break

    def example_answer(self):
        return 61229


Day.do_day(8, 2021, PartA, PartB)
