def main():
    example_data = read_input_from_file("day-10/example.txt")
    input_data = read_input_from_file("day-10/input.txt")

    print(f'Result example A: {solve_a(example_data)}\n')
    print(f'Result puzzle data A: {solve_a(input_data)}\n')
    print(f'Result example B: {solve_b(example_data)}\n')
    print(f'Result puzzle data B: {solve_b(input_data)}\n')


def read_input_from_file(file_name):
    input_file = open(file_name, "r")
    data = input_file.readlines()
    input_file.close()
    data = [x.strip() for x in data]
    return data


def solve_a(input):
    state = {
        'x': 1,
        'cycle': 1,
        'result': 0
    }
    for line in input:
        execute_instruction(state, line, handle_cycle_a)
    return state["result"]


def execute_instruction(state, instruction, handle_cycle):
    parts = instruction.split(" ")
    command = parts[0]
    match command:
        case "addx":
            handle_cycle(state, 2)
            parameter = int(parts[1])
            state["x"] += parameter
        case "noop":
            handle_cycle(state, 1)


def handle_cycle_a(state, count):
    for i in range(count):
        if is_interesting(state["cycle"]):
            state["result"] += state["cycle"] * state["x"]
        state["cycle"] += 1


def is_interesting(cycle):
    interesting_cycles = [20, 60, 100, 140, 180, 220]
    return cycle in interesting_cycles


def solve_b(input):
    state = {
        'x': 1,
        'cycle': 1,
        'crt': []
    }
    for line in input:
        execute_instruction(state, line, handle_cycle_b)
    for l in state["crt"]:
        print(l)
    print("\n")
    return


def handle_cycle_b(state, count):
    for i in range(count):
        line = (state["cycle"] - 1) // 40
        column = (state["cycle"] - 1) % 40
        if column == 0:
            state["crt"].append("")
        sprite_visible = column >= (state["x"] - 1) and column <= (state["x"] + 1)
        state["crt"][line] += "#" if sprite_visible else "."
        state["cycle"] += 1


if __name__ == "__main__":
    main()
