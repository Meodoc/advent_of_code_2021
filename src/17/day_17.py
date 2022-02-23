from aocd.models import Puzzle
from dataclasses import dataclass
from itertools import product


@dataclass
class Target:
    x1: int
    x2: int
    y1: int
    y2: int

    def within(self, x, y):
        return (x in range(self.x1, self.x2 + 1)) and (y in range(self.y1, self.y2 + 1))

    def overshot(self, x, y):
        return x > self.x2 or y < self.y1


def part_a(target: Target):
    min_, max_ = -200, 200
    tries = product(range(min_, max_), range(min_, max_))
    max_ys = set()
    for try_ in tries:
        if (max_y := sim_launch(try_[0], try_[1], target)) is not None:
            max_ys.add(max_y)

    return max(max_ys)


def part_b(target: Target):
    min_, max_ = -300, 300
    tries = product(range(min_, max_), range(min_, max_))
    hits = 0
    for try_ in tries:
        if sim_launch(try_[0], try_[1], target) is not None:
            hits += 1

    return hits


def sim_launch(vel_x: int, vel_y: int, target: Target):
    x, y = 0, 0
    max_y = 0
    while True:
        x += vel_x
        y += vel_y
        max_y = max(max_y, y)
        vel_x = vel_x if vel_x == 0 else vel_x - 1 if vel_x > 0 else vel_x + 1
        vel_y -= 1
        if target.within(x, y):
            return max_y
        if target.overshot(x, y):
            return


def load(data: str):
    data = data.split('target area: ')[-1]
    x1, x2 = data.split('x=')[-1].split(',')[0].split('..')
    y1, y2 = data.split('y=')[-1].split('..')

    return Target(int(x1), int(x2), int(y1), int(y2))


puzzle = Puzzle(year=2021, day=17)
ans_a = part_a(load(puzzle.input_data))
puzzle.answer_a = ans_a  # 4656

ans_b = part_b(load(puzzle.input_data))
puzzle.answer_b = ans_b  # 1908
