import itertools

from mylib.aoc_basics import Day
import numpy as np


class PartA(Day):
    def parse(self, text, data):
        data.jets = [-1 if char == "<" else 1 for char in text]
        data.iterate_jets = itertools.cycle(enumerate(data.jets))
        data.height = 0
        data.cave = np.zeros((512, 7), dtype=int)
        data.rocks = [
            np.array([[1, 1, 1, 1]], dtype=int),
            np.array([
                [0, 1, 0],
                [1, 1, 1],
                [0, 1, 0]], dtype=int),
            np.array([
                [1, 1, 1],
                [0, 0, 1],
                [0, 0, 1]], dtype=int),
            np.array([
                [1],
                [1],
                [1],
                [1]], dtype=int),
            np.array([
                [1, 1],
                [1, 1]], dtype=int)
        ]
        data.iterate_rocks = itertools.cycle(data.rocks)

    def compute(self, data):
        for _ in range(2022):
            rock = next(data.iterate_rocks)
            self.fall(rock, data)
        return int(data.height)

    def fall(self, rock, data):
        x = 2
        y = data.height + 3
        while True:
            if y + rock.shape[0] + 1 >= data.cave.shape[0]:
                data.cave = np.append(data.cave, np.zeros((512, 7)), axis=0)
            jet_index, dx = next(data.iterate_jets)
            x += dx
            collision = self.intersects(rock, data, x, y)
            if collision:
                x -= dx
            jet_index += 1
            y -= 1
            falling = not self.intersects(rock, data, x, y)
            if not falling:
                y += 1
                data.cave[y:y+rock.shape[0], x:x+rock.shape[1]] += rock
                data.height = max(index[0] for index in np.argwhere(data.cave == 1)) + 1
                return jet_index

    @staticmethod
    def intersects(rock, data, x, y):
        if x < 0 or x + rock.shape[1] > 7:
            return True
        if y < 0:
            return True
        return np.any(data.cave[y:y+rock.shape[0], x:x+rock.shape[1]] + rock > 1)

    def example_answer(self):
        return 3068


class PartB(PartA):
    def compute(self, data):
        round_number = 0
        complete_rounds = 0
        jet_seen = set()
        for round_number in itertools.count(1):
            rock = next(data.iterate_rocks)
            jet_index = self.fall(rock, data)
            if round_number % 5 == 0:
                if jet_index in jet_seen:
                    jet_seen = {jet_index}
                    complete_rounds += 1
                    if complete_rounds == 1:
                        height_prefix = data.height
                        round_prefix = round_number
                    elif complete_rounds == 2:
                        break
                elif complete_rounds == 0:
                    jet_seen.add(jet_index)

        height_modulo = data.height - height_prefix
        round_modulo = round_number - round_prefix

        rounds = 1000000000000

        rounds_completed = round_number

        cycle_modulo = (rounds - rounds_completed) // round_modulo
        cycle_rounds = cycle_modulo * round_modulo
        cycle_height = cycle_modulo * height_modulo

        rounds_after_cycle = rounds - rounds_completed - cycle_rounds

        for _ in range(1, rounds_after_cycle + 1):
            self.fall(next(data.iterate_rocks), data)

        return int(data.height + cycle_height)

    def example_answer(self):
        return 1514285714288


Day.do_day(17, 2022, PartA, PartB)
