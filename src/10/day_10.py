from enum import Enum

from aocd.models import Puzzle
from dataclasses import dataclass

OPEN_CHARS = {'(', '[', '{', '<'}
CLOSE_CHARS = {')', ']', '}', '>'}
PAIRS = {'(': ')', '[': ']', '{': '}', '<': '>'}
POINTS = {')': 3, ']': 57, '}': 1197, '>': 25137}

class State(Enum):
    VALID = 0,
    INCOMPLETE = 1,
    CORRUPTED = 2,

@dataclass
class Chunk:
    open: str
    close: str
    size: int
    children: list
    state: State

    def count_points(self) -> int:
        cnt = POINTS[self.close] if self.state == State.CORRUPTED else 0
        for child in self.children:
            cnt += child.count_points()
        return cnt

def part_a(code: list):
    points = 0
    for line in code:
        chunky = parse_line(line)
        points += chunky.count_points()

    print(points)
    return points

def parse_line(line: list):
    try:
        cur, nxt = line[0], line[1]
    except IndexError:
        return Chunk('x', 'y', 2, [], State.INCOMPLETE)

    if cur in CLOSE_CHARS:
        raise Exception('Closing char without opening char')

    consumed = 2
    children = []
    if nxt in OPEN_CHARS:
        while nxt not in CLOSE_CHARS:
            child = parse_line(line[consumed-1:])
            children.append(child)
            consumed += child.size
            try:
                nxt = line[consumed-1]
            except IndexError:
                return Chunk(cur, nxt, consumed, children, State.INCOMPLETE)

    # nxt in CLOSE_CHARS
    if PAIRS[cur] == nxt:
        return Chunk(cur, nxt, consumed, children, State.VALID)
    else:
        return Chunk(cur, nxt, consumed, children, State.CORRUPTED)




def load(data: str):
    return [list(line) for line in data.splitlines()]

puzzle = Puzzle(year=2021, day=10)
ans_a = part_a(load(puzzle.input_data))
print(ans_a)
puzzle.answer_a = ans_a  # 366027




with open('test.in', 'r') as f:
    test = f.read()

ans = part_a(load(test))