from aocd.models import Puzzle

import numpy as np


def part_a(data: np.ndarray):
    end = (len(data) - 1, len(data) - 1)
    distances = djikstra(data, pos=(0, 0), end=end, visited=set(), distances={(0, 0): 0})
    return distances[end]

def part_b(data: np.ndarray):
    end = (len(data) - 1, len(data) - 1)
    distances = djikstra(data, pos=(0, 0), end=end, visited=set(), distances={(0, 0): 0})
    return distances[data.shape[0]-1, data.shape[1]-1]


def djikstra(risk_map: np.ndarray, pos: tuple, end: tuple, visited: set, distances: dict):
    while pos != end:
        visited.add(pos)

        for adj in get_adj(risk_map, *pos):
            if adj not in visited:
                new_dist = distances[pos] + risk_map[adj]
                distances[adj] = min(distances[adj], new_dist) if adj in distances else new_dist

        dist_unvisited = {k: v for k, v in distances.items() if k not in visited}
        pos = min(dist_unvisited, key=dist_unvisited.get)

    return distances


def get_adj(matrix: np.ndarray, x: int, y: int):
    adj = [(x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)]
    return [(x, y) for x, y in adj if 0 <= x < matrix.shape[0] and 0 <= y < matrix.shape[1]]


def load(data: str, full=False):
    risk_map = np.array([list(map(int, line)) for line in data.splitlines()])
    if full:
        expand_vert = [((risk_map.copy() - 1 + i) % 9) + 1 for i in range(1, 5)]
        risk_map = np.concatenate((risk_map, *expand_vert), axis=0)
        expand_horiz = [((risk_map.copy() - 1 + i) % 9) + 1 for i in range(1, 5)]
        risk_map = np.concatenate((risk_map, *expand_horiz), axis=1)
    return risk_map


puzzle = Puzzle(year=2021, day=15)
ans_a = part_a(load(puzzle.input_data))
print(ans_a)
# puzzle.answer_a = ans_a  # 717

ans_b = part_b(load(puzzle.input_data, full=True))
print(ans_b)
# puzzle.answer_b = ans_b  # 2993

# with open ('test.in') as f:
#     test = f.read()
#
# ans = part_a(load(test, full=True))
# print(ans)
