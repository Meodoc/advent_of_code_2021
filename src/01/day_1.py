from aocd.models import Puzzle
from funcy import lmap


def part_a(data: list):
    cnt = 0
    for i in range(len(data) - 1):
        if data[i + 1] > data[i]:
            cnt += 1
    return cnt


def part_b(data: list):
    cnt = 0
    for i in range(len(data) - 3):
        if sum(data[i + 1:i + 4]) > sum(data[i:i + 3]):
            cnt += 1
    return cnt


def load(data: str):
    return lmap(int, data.split())


puzzle = Puzzle(year=2021, day=1)
# puzzle.answer_a = part_a(load(puzzle.input_data))
# puzzle.answer_b = part_b(load(puzzle.input_data))
