import numpy as np
import os


def read_input_from_file(file_name: str) -> list:
    script_path = os.path.dirname(os.path.abspath(__file__))
    input_file = open(f"{script_path}/{file_name}", "r")
    data = input_file.readlines()
    data = [x.strip() for x in data]
    input_file.close()
    return data


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


def apply_enhancement(image: np.ndarray, enhancement: str, step: int) -> np.ndarray:
    new_image = np.empty((image.shape[0] + 2, image.shape[1] + 2), dtype=int)
    for y in range(-1, image.shape[0] + 1):
        for x in range(-1, image.shape[1] + 1):
            filler = 0 if enhancement[0] == "." else step % 2
            index = get_index(image, x, y, filler)
            new_image[1 + y, 1 + x] = 0 if enhancement[index] == "." else 1
    return new_image


def print_image(image) -> None:
    for row in image:
        print("".join(["." if x == 0 else "#" for x in row]))
    print("")


def run(data: list, steps: int) -> None:
    enhancement = data[0]
    image = [list(line) for line in data[2:]]
    image = np.array(image)
    image = np.where(image == ".", 0, 1)

    for step in range(steps):
        image = apply_enhancement(image, enhancement, step)
    lit = np.count_nonzero(image)
    print(f"lit pixels: {lit}")


def main() -> None:
    example_data = read_input_from_file("example.txt")
    data = read_input_from_file("input.txt")

    print("Example Part 1")
    run(example_data, 2)
    print("Input data Part 1")
    run(data, 2)

    print("Example Part 2")
    run(example_data, 50)
    print("Input data Part 2")
    run(data, 50)


if __name__ == "__main__":
    main()
