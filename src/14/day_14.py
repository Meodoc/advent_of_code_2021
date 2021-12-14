from aocd.models import Puzzle
from more_itertools import windowed
from collections import defaultdict


def part_a(template: str, rules: dict):  # naive solution for part a
    for _ in range(10):
        i = 1
        for pair in windowed(template, 2):
            template = template[:i] + rules[''.join(pair)] + template[i:]
            i += 2
    most, least = max(set(template), key=template.count), min(set(template), key=template.count)
    return template.count(most) - template.count(least)


def part_b(template: str, rules: dict):
    pairs = [''.join(pair) for pair in windowed(template, 2)]
    pair_counts = defaultdict(int, {pair: pairs.count(pair) for pair in pairs})
    poly_counts = defaultdict(int, {poly: template.count(poly) for poly in template})

    for _ in range(40):
        pair_counts_step = pair_counts.copy()
        for match, insert in rules.items():
            n_match = pair_counts[match]

            insert_left, insert_right = match[0] + insert, insert + match[1]
            pair_counts_step[insert_left] += n_match
            pair_counts_step[insert_right] += n_match
            pair_counts_step[match] -= n_match

            poly_counts[insert] += n_match

        pair_counts = pair_counts_step

    return max(poly_counts.values()) - min(poly_counts.values())


def load(data: str):
    template, rules = data.split('\n\n')
    return template, {rule.split(' -> ')[0]: rule.split(' -> ')[1] for rule in rules.splitlines()}


puzzle = Puzzle(year=2021, day=14)
ans_a = part_a(*load(puzzle.input_data))
# puzzle.answer_a = ans_a  # 3095
ans_b = part_b(*load(puzzle.input_data))
print(ans_b)
# puzzle.answer_b = ans_b  # 3152788426516
