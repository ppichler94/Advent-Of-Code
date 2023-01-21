import re

from mylib.aoc_basics import Day


class PartA(Day):
    def parse(self, text, data):
        passport_texts = text.split("\n\n")
        data.passports = [self.parse_passport(p) for p in passport_texts]

    @staticmethod
    def parse_passport(text):
        matches = [re.match(r"(.*):(.*)", part) for part in text.replace("\n", " ").split(" ")]
        return dict((match.group(1), match.group(2)) for match in matches)

    def compute(self, data):
        return sum(1 if self.validate_passport(passport) else 0 for passport in data.passports)

    def validate_passport(self, passport):
        required = ("byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid")
        return all(x in passport.keys() for x in required)

    def example_answer(self):
        return 2


class PartB(PartA):
    def validate_passport(self, passport):
        required = ("byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid")
        if not all(x in passport.keys() for x in required):
            return False
        if not 1920 <= int(passport["byr"]) <= 2002:
            return False
        if not 2010 <= int(passport["iyr"]) <= 2020:
            return False
        if not 2020 <= int(passport["eyr"]) <= 2030:
            return False
        if match := re.match(r"(\d+)cm", passport["hgt"]):
            if not 150 <= int(match.group(1)) <= 193:
                return False
        elif match := re.match(r"(\d+)in", passport["hgt"]):
            if not 59 <= int(match.group(1)) <= 76:
                return False
        else:
            return False
        if not re.match(r"#(\d|[a-f]){6}", passport["hcl"]):
            return False
        if passport["ecl"] not in ("amb", "blu", "brn", "gry", "grn", "hzl", "oth"):
            return False
        if not re.match(r"^\d{9}$", passport["pid"]):
            return False
        return True

    def example_answer(self):
        return 4

    def get_example_input(self, puzzle):
        return """
pid:087499704 hgt:74in ecl:grn iyr:2020 eyr:2022 byr:2002
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719

eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007
"""


Day.do_day(4, 2020, PartA, PartB)
