from collections import namedtuple


def main():
    example_data = read_input_from_file("day-07/example.txt")
    input_data = read_input_from_file("day-07/input.txt")

    print(f'Result example A: {solve_a(example_data)}\n')
    print(f'Result puzzle data A: {solve_a(input_data)}\n')
    print(f'Result example B: {solve_b(example_data)}\n')
    print(f'Result puzzle data B: {solve_b(input_data)}\n')


File = namedtuple("File", ["name", "size"])


class Directory:
    def __init__(self):
        self.directories = []
        self.files = []
        self.name = "_"
        self.parent = None

    def size(self):
        size = 0
        for file in self.files:
            size += file.size
        for directory in self.directories:
            size += directory.size()
        return size


def read_input_from_file(file_name):
    input_file = open(file_name, "r")
    data = input_file.readlines()
    input_file.close()
    data = [x.strip() for x in data]
    return data


def solve_a(input):
    root = parse_commands(input)
    sizes = []
    calculate_sizes(root, sizes)
    return sum([s for s in sizes if s <= 100000])


def parse_commands(input):
    current_dir = Directory()
    current_dir.name = "root"
    for i in range(1, len(input)):
        line = input[i]
        match line.split(" "):
            case ["$", "ls"]:
                parse_ls(input[i+1:], current_dir)
            case ["$", "cd", ".."]:
                current_dir = current_dir.parent
            case ["$", "cd", name]:
                current_dir = [d for d in current_dir.directories if d.name == name][0]
    return find_root(current_dir)


def parse_ls(input, current_dir):
    for line in input:
        if line[0] == "$":
            return
        if line[0:3] == "dir":
            d = Directory()
            d.name = line[4:]
            d.parent = current_dir
            current_dir.directories.append(d)
        else:
            parts = line.split(" ")
            current_dir.files.append(File(parts[1], int(parts[0])))


def find_root(direcotry):
    d = direcotry
    while d.parent:
        d = d.parent
    return d


def calculate_sizes(direcotry, sizes):
    sizes.append(direcotry.size())
    for d in direcotry.directories:
        calculate_sizes(d, sizes)


def solve_b(input):
    root = parse_commands(input)
    sizes = []
    calculate_sizes(root, sizes)
    required_size = 30000000 - (70000000 - root.size())
    result = {"size": root.size()}
    find_dir_to_delete(required_size, root, result)
    return result["size"]


def find_dir_to_delete(required_size, directory, result):
    direcotry_size = directory.size()
    if direcotry_size >= required_size and direcotry_size < result["size"]:
        result["size"] = direcotry_size
    for d in directory.directories:
        find_dir_to_delete(required_size, d, result)


if __name__ == "__main__":
    main()
