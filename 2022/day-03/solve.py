from mylib.aoc_basics import Day


class PartA(Day):
    def compute(self, data):
        priority_sum = 0
        for line in data.text.splitlines():
            size = len(line)
            compartment_size = int(size / 2)
            list_a = line[:compartment_size]
            list_b = line[compartment_size:]
            common_item = PartA.find_common_item(list_a, list_b)
            priority_sum += PartA.priority_of(common_item)
        return priority_sum

    @classmethod
    def find_common_item(cls, *lists):
        return set.intersection(*map(set, lists)).pop()

    @classmethod
    def priority_of(cls, item):
        if ord('a') <= ord(item) <= ord('z'):
            return 1 + ord(item) - ord('a')
        elif ord('A') <= ord(item) <= ord('Z'):
            return 27 + ord(item) - ord('A')


class PartB(PartA):
    def compute(self, data):
        priority_sum = 0
        lines = data.text.splitlines()
        for i in range(0, len(lines), 3):
            badge = PartA.find_common_item(*lines[i:i+3])
            priority_sum += PartA.priority_of(badge)
        return priority_sum


Day.do_day(3, 2022, PartA, PartB)
