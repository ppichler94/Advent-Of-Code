import numpy as np
from mylib.aoc_basics import Day


class PartA(Day):
    def parse(self, text, data):
        enhancement_text, image_text = text.split("\n\n")
        data.enhancement = enhancement_text.replace("\n", "")
        data.image = np.array([[1 if c == "#" else 0 for c in line] for line in image_text.splitlines()])
        data.steps = 2

    def compute(self, data):
        for step in range(data.steps):
            data.image = self.apply_enhancement(data.image, data.enhancement, step)
        return np.count_nonzero(data.image)

    def apply_enhancement(self, image: np.ndarray, enhancement: str, step: int) -> np.ndarray:
        new_image = np.empty((image.shape[0] + 2, image.shape[1] + 2), dtype=int)
        for y in range(-1, image.shape[0] + 1):
            for x in range(-1, image.shape[1] + 1):
                filler = 0 if enhancement[0] == "." else step % 2
                index = self.get_index(image, x, y, filler)
                new_image[1 + y, 1 + x] = 0 if enhancement[index] == "." else 1
        return new_image

    @staticmethod
    def get_index(image: np.ndarray, x: int, y: int, filler: int) -> int:
        index = []
        for yi in range(-1, 2):
            for xi in range(-1, 2):
                if x + xi < 0 or x + xi >= image.shape[1]:
                    index.append(filler)
                elif y + yi < 0 or y + yi >= image.shape[0]:
                    index.append(filler)
                else:
                    index.append(image[y + yi, x + xi])
        return int("".join(str(x) for x in index), 2)

    def example_answer(self):
        return 35


class PartB(PartA):
    def part_config(self, data):
        data.steps = 50

    def example_answer(self):
        return 3351


Day.do_day(20, 2021, PartA, PartB)
