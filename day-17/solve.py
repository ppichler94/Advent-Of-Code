from mylib.aoc_basics import Day
import numpy as np

class PartA(Day):
    def part_config(self, data):
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
        data.cave = np.zeros((512, 7), dtype=int)

    def compute(self, data):
        y_max = -1
        jet_index = 0
        for i in range(2022):
            rock = data.rocks[i % 5]
            x = 2
            y = y_max + 4
            while True:
                if y + rock.shape[0] + 1 >= data.cave.shape[0]:
                    data.cave = np.append(data.cave, np.zeros((512, 7)), axis=0)
                x += self.get_jet(data, jet_index)
                collision = self.intersects(data, rock, x, y)
                if collision:
                    x -= self.get_jet(data, jet_index)
                jet_index += 1
                y -= 1
                falling = not self.intersects(data, rock, x, y)
                if not falling:
                    y += 1
                    data.cave[y:y+rock.shape[0], x:x+rock.shape[1]] += rock
                    y_max = max(index[0] for index in np.argwhere(data.cave == 1))
                    break
        return int(y_max + 1)

    def get_jet(self, data, index):
        character = data.text[index % len(data.text)]
        return -1 if character == "<" else 1

    def intersects(self, data, rock, x, y):
        if x < 0 or x + rock.shape[1] > 7:
            return True
        if y < 0:
            return True
        return np.any(data.cave[y:y+rock.shape[0], x:x+rock.shape[1]] + rock > 1)

    def print_cave(self, cave, y_max):
        print("")
        for y in range(y_max, -1, -1):
            print(''.join([{0: ".", 1: "#"}.get(v) for v in cave[y, :]]))
        print("")

    def example_answer(self):
        return 3068


class PartB(PartA):
    def example_answer(self):
        return 1514285714288


Day.do_day(17, 2022, PartA, PartB)
