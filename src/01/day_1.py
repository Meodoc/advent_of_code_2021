from aocd.models import Puzzle
from funcy import lmap


def part_a(data: list):
    return sum(x[1] > x[0] for x in zip(data, data[1:]))


def part_b(data: list):
    return sum(x[1] > x[0] for x in zip(data, data[3:]))


def load(data: str):
    return lmap(int, data.split())


puzzle = Puzzle(year=2021, day=1)
# puzzle.answer_a = part_a(load(puzzle.input_data))  # 1292
# puzzle.answer_b = part_b(load(puzzle.input_data))  # 1262
