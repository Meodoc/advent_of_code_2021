from aocd.models import Puzzle
from funcy import lmap


def part_a(data: list):
    fish = [data.count(i) for i in range(9)]
    return simulate(fish, iterations=80)


def part_b(data: list):
    fish = [data.count(i) for i in range(9)]
    return simulate(fish, iterations=256)


def simulate(fish: list, iterations: int):
    for _ in range(iterations):
        birth = fish.pop(0)
        fish.append(0)
        fish[6] += birth
        fish[8] += birth
    return sum(fish)


def load(data: str):
    return lmap(int, data.split(','))


puzzle = Puzzle(year=2021, day=6)
ans_a = part_a(load(puzzle.input_data))
# puzzle.answer_a = ans_a  # 343441
ans_b = part_b(load(puzzle.input_data))
# puzzle.answer_b = ans_b  # 1569108373832
