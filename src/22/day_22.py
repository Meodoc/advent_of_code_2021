from aocd.models import Puzzle
from funcy import lmap
from dataclasses import dataclass, field

import numpy as np


# Credit for solution (part b): https://github.com/rnbwdsh/advent-of-code/blob/master/aoc21.ipynb


@dataclass
class Cuboid:
    x: range
    y: range
    z: range
    state: int

    overlap: list = field(default_factory=list)

    def handle_overlap(self, other: 'Cuboid'):
        overlap_x = range(max(self.x[0], other.x[0]), min(self.x[-1] + 1, other.x[-1] + 1))
        overlap_y = range(max(self.y[0], other.y[0]), min(self.y[-1] + 1, other.y[-1] + 1))
        overlap_z = range(max(self.z[0], other.z[0]), min(self.z[-1] + 1, other.z[-1] + 1))

        if overlap_x and overlap_y and overlap_z:
            new_overlap = Cuboid(overlap_x, overlap_y, overlap_z, False)

            # determine overlaps with already overlapping cubes
            for overlap in self.overlap:
                overlap.handle_overlap(new_overlap)

            self.overlap.append(new_overlap)

    def count_cubes(self):
        return (len(self.x) * len(self.y) * len(self.z)) - sum(overlap.count_cubes() for overlap in self.overlap)


# naive array solution for part a
def part_a(instructions: list):
    reactor = np.zeros((101, 101, 101), np.bool8)
    for x, y, z, init in instructions:
        if x[0] < -50 or y[0] < -50 or z[0] < -50 or x[1] > 50 or y[1] > 50 or z[1] > 50:
            continue

        # normalize coords
        x = (x[0] + 50, x[1] + 50)
        y = (y[0] + 50, y[1] + 50)
        z = (z[0] + 50, z[1] + 50)

        reactor[x[0]: x[1] + 1, y[0]: y[1] + 1, z[0]: z[1] + 1] = init

    return np.count_nonzero(reactor)


def part_b(instructions: list):
    cuboids = []

    for x, y, z, init in instructions:
        new_cube = Cuboid(range(x[0], x[1] + 1), range(y[0], y[1] + 1), range(z[0], z[1] + 1), init)
        for cube in cuboids:
            cube.handle_overlap(new_cube)
        cuboids.append(new_cube)

    return sum(c.count_cubes() for c in cuboids if c.state)


def load(data: str):
    instructions = []
    for instr in data.splitlines():
        init = instr.split()[0] == 'on'
        x, y, z = instr.split()[1].split(',')
        x, y, z = lmap(int, x[2:].split('..')), lmap(int, y[2:].split('..')), lmap(int, z[2:].split('..'))
        instructions.append((x, y, z, init))
    return instructions


puzzle = Puzzle(year=2021, day=22)
# ans_a = part_a(load(puzzle.input_data))
# print(ans_a)
# puzzle.answer_a = ans_a  # 596598

# ans_b = part_b(load(puzzle.input_data))
# print(ans_b)
# puzzle.answer_b = ans_b  # 1199121349148621

