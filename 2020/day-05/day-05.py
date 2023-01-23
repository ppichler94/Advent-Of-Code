from mylib.aoc_basics import Day


class PartA(Day):
    def parse(self, text, data):
        data.passes = text.splitlines()

    def compute(self, data):
        ids = self.calculate_ids(data)
        return max(ids)

    @staticmethod
    def calculate_ids(data):
        ids = []
        for boarding_pass in data.passes:
            row = (0, 127)
            column = (0, 7)
            for c in boarding_pass:
                match c:
                    case "F":
                        row = (row[0], (row[1] + row[0]) // 2)
                    case "B":
                        row = ((row[1] + row[0]) // 2, row[1])
                    case "L":
                        column = (column[0], (column[1] + column[0]) // 2)
                    case "R":
                        column = ((column[1] + column[0]) // 2, column[1])
            ids.append(row[1] * 8 + column[1])
        return ids

    def example_answer(self):
        return 820

    def get_example_input(self, puzzle):
        return "BFFFBBFRRR\nFFFBBBFRRR\nBBFFBBFRLL"


class PartB(PartA):
    def compute(self, data):
        ids = self.calculate_ids(data)
        ids = list(sorted(ids))
        for a, b in zip(ids, ids[1:]):
            if a + 2 == b:
                return a + 1
        return "No result"

    def get_example_input(self, puzzle):
        return None


Day.do_day(5, 2020, PartA, PartB)
