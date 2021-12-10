from aocd.models import Puzzle
from funcy import lmap
from statistics import median, mean


def part_a(data: list):
    mid = int(median(data))
    return sum(abs(mid - pos) for pos in data)


def part_b(data: list):
    mid = int(mean(data))
    return sum(gauss_sum(abs(mid - pos)) for pos in data)


def gauss_sum(n):
    return (n * (n + 1)) // 2


def load(data: str):
    return lmap(int, data.split(','))


puzzle = Puzzle(year=2021, day=7)
ans_a = part_a(load(puzzle.input_data))
# puzzle.answer_a = ans_a  # 344605
ans_b = part_b(load(puzzle.input_data))
# puzzle.answer_b = ans_b  # 93699985
