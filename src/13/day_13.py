from aocd.models import Puzzle
from funcy import lmap

import numpy as np
import matplotlib.pyplot as plt


def part_a(paper: np.ndarray, instructions: list):
    paper = fold_paper(paper, instructions, only_first=True)
    return np.sum(paper)


def part_b(paper: np.ndarray, instructions: list):
    paper = fold_paper(paper, instructions)
    plt.imshow(paper)
    plt.show()


def fold_paper(paper: np.ndarray, instructions: list, only_first=False):
    if only_first:
        instructions = instructions[:1]
    for axis, pos in instructions:
        pos = int(pos)
        if axis == 'y':
            a, b = paper[:pos], np.flipud(paper)[:pos]
        else:
            a, b = paper[:,:pos], np.fliplr(paper)[:,:pos]
        paper = a | b

    return paper


def load(data: str):
    dots, instrs = data.split('\n\n')
    dots = [lmap(int, dot.split(',')) for dot in dots.splitlines()]
    instrs = [instr.replace('fold along ', '').split('=') for instr in instrs.splitlines()]

    max_x, max_y = np.amax(dots, axis=0)
    paper_dims = (max_y + 2, max_x + 1)  # randomly have to add +2 instead of +1 to the y dimension to get a readable solution
    paper = np.zeros(paper_dims, dtype=bool)
    for x, y in dots:
        paper[y, x] = True
    return paper, instrs


puzzle = Puzzle(year=2021, day=13)
ans_a = part_a(*load(puzzle.input_data))
# puzzle.answer_a = ans_a  # 788
part_b(*load(puzzle.input_data))  # KJBKEUBG
