from aocd.models import Puzzle

import numpy as np

def part_a(data: list):
    data = np.array(data)
    gamma = (np.sum(data, axis=0) > (data.shape[0] / 2)).astype(int)
    epsilon = 1 - gamma
    return bitarr_to_int(gamma) * bitarr_to_int(epsilon)

def part_b(data: list):
    oxygen, co2 = np.array(data), np.array(data)

    for c in range(oxygen.shape[1]):
        mcv = sum(oxygen[:,c]) >= (oxygen.shape[0] / 2)
        rem_idx = [r for r in range(oxygen.shape[0]) if oxygen[r,c] != mcv]
        oxygen = np.delete(oxygen, rem_idx, axis=0)
        if oxygen.shape[0] == 1:
            break

    for c in range(co2.shape[1]):
        lcv = sum(co2[:,c]) < (co2.shape[0] / 2)
        rem_idx = [r for r in range(co2.shape[0]) if co2[r,c] != lcv]
        co2 = np.delete(co2, rem_idx, axis=0)
        if co2.shape[0] == 1:
            break

    return bitarr_to_int(oxygen[0]) * bitarr_to_int(co2[0])

def bitarr_to_int(bitarr: np.ndarray):
    return int(''.join(bitarr.astype(str)), 2)

def load(data: str):
    return [list(map(int, b)) for b in data.splitlines()]

puzzle = Puzzle(year=2021, day=3)
ans_a = part_a(load(puzzle.input_data))
#puzzle.answer_a = ans_a  # 741950
ans_b = part_b(load(puzzle.input_data))
#puzzle.answer_b = ans_b  # 903810
