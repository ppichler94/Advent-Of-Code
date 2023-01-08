import numpy as np
from mylib.aoc_basics import Day


class PartA(Day):
    def parse(self, text, data):
        data.cave = np.zeros([500, 1000], dtype=int)
        for line in text.splitlines():
            parts = line.split(" -> ")
            for i in range(len(parts) - 1):
                x1 = int(parts[i].split(",")[0])
                y1 = int(parts[i].split(",")[1])
                x2 = int(parts[i+1].split(",")[0])
                y2 = int(parts[i+1].split(",")[1])

                x_start = min(x1, x2)
                x_end = max(x1, x2) + 1
                y_start = min(y1, y2)
                y_end = max(y1, y2) + 1

                data.cave[y_start:y_end,x_start:x_end] = 1
        data.max_y = np.max(np.argwhere(data.cave == 1), axis=0)[0]

    def compute(self, data):
        sand_resting = True
        while sand_resting:
            sand_resting = PartA.add_sand(data)
        return np.count_nonzero(data.cave == 2)

    @staticmethod
    def add_sand(data):
        x = 500
        y = 0
        while 1:
            if y > data.max_y:
                return False
            if data.cave[y + 1, x] == 0:
                y += 1
            elif data.cave[y + 1, x - 1] == 0:
                y += 1
                x -= 1
            elif data.cave[y + 1, x + 1] == 0:
                y += 1
                x += 1
            else:
                data.cave[y, x] = 2
                return True

    def example_answer(self):
        return 24


class PartB(PartA):
    def compute(self, data):
        data.cave[data.max_y + 2, 0:1000] = 1
        data.max_y += 3
        while 1:
            PartA.add_sand(data)
            if data.cave[0, 500] == 2:
                break
        return np.count_nonzero(data.cave == 2)

    def example_answer(self):
        return 93


Day.do_day(14, 2022, PartA, PartB)
