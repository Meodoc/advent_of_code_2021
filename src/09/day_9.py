from aocd.models import Puzzle
from math import prod

import numpy as np

BOUNDARY = 9

def part_a(data: np.ndarray):
    data = np.pad(data, pad_width=1, mode='maximum')
    return sum(data[low] + 1 for low in find_low_points(data))


def part_b(data: np.ndarray):
    data = np.pad(data, pad_width=1, mode='maximum')
    low_points = find_low_points(data)
    basin_sizes = [basin_size(data, low_point, visited=set()) for low_point in low_points]
    basin_sizes.sort(reverse=True)
    return prod(basin_sizes[:3])


def find_low_points(data: np.ndarray):
    low_points = []
    for x in range(1, data.shape[0] - 1):
        for y in range(1, data.shape[1] - 1):
            if data[x, y] < data[x - 1, y] and data[x, y] < data[x + 1, y] and data[x, y] < data[x, y - 1] and data[x, y] < data[x, y + 1]:
                low_points.append((x, y))
    return low_points


def basin_size(data: np.ndarray, pos: tuple, visited: set, size: int = 1):
    if pos in visited or data[pos] == BOUNDARY:
        return 0
    visited.add(pos)
    x, y = pos
    size += basin_size(data, (x + 1, y), visited) + \
            basin_size(data, (x - 1, y), visited) + \
            basin_size(data, (x, y + 1), visited) + \
            basin_size(data, (x, y - 1), visited)
    return size


def load(data: str):
    return np.array([list(map(int, line)) for line in data.splitlines()])


puzzle = Puzzle(year=2021, day=9)
ans_a = part_a(load(puzzle.input_data))
# puzzle.answer_a = ans_a  # 591
ans_b = part_b(load(puzzle.input_data))
# puzzle.answer_b = ans_b  # 1113424
