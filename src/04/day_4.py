from aocd.models import Puzzle
from funcy import lmap

import numpy as np

def part_a(draws: list, boards: np.ndarray):
    draw, board, mask = play(draws, boards, mask=np.zeros_like(boards), first_win=True)
    return np.ma.masked_array(board, mask).sum() * draw

def part_b(draws: list, boards: np.ndarray):
    draw, board, mask = play(draws, boards, mask=np.zeros_like(boards), first_win=False)
    return np.ma.masked_array(board, mask).sum() * draw

def play(draws: list, boards: np.ndarray, mask: np.ndarray, first_win: bool):
    def _check_win(marked_: int):
        cols, rows = np.sum(marked_, axis=0), np.sum(marked_, axis=1)
        return 5 in cols or 5 in rows

    for draw in draws:
        winners = []
        mask[np.nonzero(boards == draw)] = 1
        for i, marked in enumerate(mask):
            if i not in winners and _check_win(marked):
                if first_win:
                    return draw, boards[i], mask[i]
                winners.append(i)
        if len(winners) == len(boards):
            return draw, boards[winners[-1]], mask[winners[-1]]

def load(data: str):
    drawing = lmap(int, data.split()[0].split(','))
    boards = np.array([[lmap(int, row.split()) for row in board.splitlines()] for board in data.split('\n\n')[1:]])
    return drawing, boards


puzzle = Puzzle(year=2021, day=4)
ans_a = part_a(*load(puzzle.input_data))
#puzzle.answer_a = ans_a  # 71708
ans_b = part_b(*load(puzzle.input_data))
#puzzle.answer_b = ans_b  # 34726
