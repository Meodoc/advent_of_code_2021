from aocd.models import Puzzle
from itertools import product

import numpy as np


def part_a(data: np.ndarray):
    return simulate(data, count=True)


def part_b(data: np.ndarray):
    return simulate(data)


def simulate(energy: np.ndarray, count: bool = False, iterations: int = 100):
    flashes, i = 0, 0
    while True:
        i += 1

        flashed = set()
        energy += 1
        while len(flash := tuple(tuple(pos) for pos in np.argwhere(energy > 9) if tuple(pos) not in flashed)) > 0:
            flashed.update(flash)
            for x, y in flash:
                for pos in get_adj(x, y, len(energy)):
                    energy[pos] += 1
        for flash in flashed:
            energy[flash] = 0
        flashes += len(flashed)

        if count and i == iterations:
            return flashes
        elif not count and np.all(energy == 0):
            return i


def get_adj(x: int, y: int, size: int):
    adj = list(product(range(x - 1, x + 2), range(y - 1, y + 2)))
    return ((x, y) for x, y in adj if 0 <= x < size and 0 <= y < size)


def load(data: str):
    return np.array([list(map(int, line)) for line in data.splitlines()])


puzzle = Puzzle(year=2021, day=11)
ans_a = part_a(load(puzzle.input_data))
# puzzle.answer_a = ans_a  # 1667
ans_b = part_b(load(puzzle.input_data))
# puzzle.answer_b = ans_b  # 488
