from aocd.models import Puzzle

def part_a(data: list):
    pos = 0 + 0j
    for direction, steps in data:
        match direction:
            case 'forward': pos += steps
            case 'down': pos += steps * 1j
            case 'up': pos -= steps * 1j
    return int(pos.real * pos.imag)

def part_b(data: list):
    pos, aim = 0 + 0j, 0
    for direction, steps in data:
        match direction:
            case 'forward': pos += steps + (aim * steps * 1j)
            case 'down': aim += steps
            case 'up': aim -= steps
    return int(pos.real * pos.imag)

def load(data: str):
    return [(d, int(s)) for d, s in (l.split() for l in data.splitlines())]

puzzle = Puzzle(year=2021, day=2)
ans_a = part_a(load(puzzle.input_data))
#puzzle.answer_a = ans_a  # 1561344
ans_b = part_b(load(puzzle.input_data))
#puzzle.answer_b = ans_b  # 1848454425