from enum import Enum
from aocd.models import Puzzle
from dataclasses import dataclass

OPEN_CHARS = {'(', '[', '{', '<'}
CLOSE_CHARS = {')', ']', '}', '>'}
PAIRS = {'(': ')', '[': ']', '{': '}', '<': '>'}
CORRUPTION_POINTS = {')': 3, ']': 57, '}': 1197, '>': 25137}
INCOMPLETENESS_POINTS = {')': 1, ']': 2, '}': 3, '>': 4}


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

    def is_corrupted(self) -> bool:
        corrupted = self.state == State.CORRUPTED or any(child.is_corrupted() for child in self.children)
        return corrupted

    def corruption_score(self) -> int:
        score = CORRUPTION_POINTS[self.close] if self.state == State.CORRUPTED else 0
        score += sum(child.corruption_score() for child in self.children)
        return score

    def incompleteness_score(self) -> int:
        score = 0
        score += sum(child.incompleteness_score() for child in self.children)
        if self.state == State.INCOMPLETE:
            score *= 5
            score += INCOMPLETENESS_POINTS[self.close]
        return score


def part_a(code: list):
    points = 0
    for line in code:
        chunks = parse_line(line)
        points += sum(chunk.corruption_score() for chunk in chunks)
    return points


def part_b(code: list):
    incomplete_lines = [parse_line(line) for line in code if not any(chunk.is_corrupted() for chunk in parse_line(line))]

    points = []
    for line in incomplete_lines:
        points.append(sum(chunk.incompleteness_score() for chunk in line))
    points = sorted(points)
    return points[len(points) // 2]


def parse_line(line: list):
    def parse(line_: list):
        try:
            cur, nxt = line_[0], line_[1]
        except IndexError:
            return Chunk(line_[0], PAIRS[line_[0]], 2, [], State.INCOMPLETE)

        consumed = 2
        children = []
        while nxt not in CLOSE_CHARS:
            child = parse(line_[consumed - 1:])
            children.append(child)
            consumed += child.size
            try:
                nxt = line_[consumed - 1]
            except IndexError:
                return Chunk(cur, PAIRS[cur], consumed, children, State.INCOMPLETE)

        # nxt in CLOSE_CHARS
        if PAIRS[cur] == nxt:
            return Chunk(cur, nxt, consumed, children, State.VALID)
        else:
            return Chunk(cur, nxt, consumed, children, State.CORRUPTED)

    chunks = []
    total_consumed = 0
    while total_consumed < len(line):
        chunk = parse(line[total_consumed:])
        chunks.append(chunk)
        total_consumed += chunk.size
    return chunks


def load(data: str):
    return [list(line) for line in data.splitlines()]


puzzle = Puzzle(year=2021, day=10)
ans_a = part_a(load(puzzle.input_data))
print(ans_a)
# puzzle.answer_a = ans_a  # 366027

ans_b = part_b(load(puzzle.input_data))
print(ans_b)
# puzzle.answer_b = ans_b  # 1118645287
