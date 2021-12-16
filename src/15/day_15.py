from aocd.models import Puzzle

import numpy as np

def part_a(data: np.ndarray):
    distances = djikstra(data, (0, 0), visited=set(), distances={(0,0): 0}, path=[])
    print("Finished")
    print(distances)
    # print(path)
    # print(sum(data[p] for p in path))
    return distances

def djikstra(risk_map: np.ndarray, pos: tuple, visited: set, distances: dict, path: list, depth=0):
    # if pos == (len(risk_map),len(risk_map)):
    #     return

    visited.add(pos)
    for adj in get_adj(risk_map,*pos):
        if adj not in visited:
            if adj in distances:
                distances[adj] = min(distances[adj], distances[pos] + risk_map[adj])
            else:
                distances[adj] = distances[pos] + risk_map[adj]


    next_cand = {k:v for k, v in distances.items() if k not in visited}

    if len(next_cand) == 0:
        return

    next_ = min(next_cand, key=next_cand.get)
    djikstra(risk_map, next_, visited, distances, path, depth + 1)

    return distances[(9,9)]


def get_adj(matrix: np.ndarray, x: int, y: int):
    adj = [(x,y+1),(x,y-1),(x+1,y),(x-1,y)]
    return [(x, y) for x, y in adj if 0 <= x < matrix.shape[0] and 0 <= y < matrix.shape[1]]


def load(data: str):
    return np.array([list(map(int, line)) for line in data.splitlines()])

puzzle = Puzzle(year=2021, day=15)
# ans_a = part_a(load(puzzle.input_data))
# print(ans_a)
# puzzle.answer_a = ans_a


with open ('test.in') as f:
    test = f.read()

ans = part_a(load(test))
print(ans)