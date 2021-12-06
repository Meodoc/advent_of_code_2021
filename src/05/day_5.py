from aocd.models import Puzzle
from funcy import lmap

import numpy as np
import re


def part_a(data: np.ndarray):
    x_max, y_max = np.max(data[:, :, 0]), np.max(data[:, :, 1])
    diagram = draw_lines(data, diagram=np.zeros((x_max + 1, y_max + 1)), diagonal=False)
    return np.count_nonzero(diagram >= 2)


def part_b(data: np.ndarray):
    x_max, y_max = np.max(data[:, :, 0]), np.max(data[:, :, 1])
    diagram = draw_lines(data, diagram=np.zeros((x_max + 1, y_max + 1)), diagonal=True)
    return np.count_nonzero(diagram >= 2)


def draw_lines(data: np.ndarray, diagram: np.ndarray, diagonal: bool):
    for x, y in data[0]:
        x_diff, y_diff = abs(x[0] - x[1]), abs(y[0] - y[1])
        if not diagonal and x_diff != 0 and y_diff != 0:
            continue
        line_x = interpolate(x[0], x[1]) if x_diff != 0 else [x[0]] * (y_diff + 1)
        line_y = interpolate(y[0], y[1]) if y_diff != 0 else [y[0]] * (x_diff + 1)
        markings = list(zip(line_y, line_x))
        for marking in markings:
            diagram[marking] += 1
    return diagram


def interpolate(v0: int, v1: int):
    return range(v0, v1 + 1, 1) if v0 <= v1 else range(v0, v1 - 1, -1)


def load(data: str):
    x_points = [lmap(int, re.split(' -> |,', line)[0:3:2]) for line in data.splitlines()]
    y_points = [lmap(int, re.split(' -> |,', line)[1:4:2]) for line in data.splitlines()]
    return np.array(list(zip(x_points, y_points)))


puzzle = Puzzle(year=2021, day=5)
ans_a = part_a(load(puzzle.input_data))
# puzzle.answer_a = ans_a  # 6548
ans_b = part_b(load(puzzle.input_data))
# puzzle.answer_b = ans_b  # 19663
