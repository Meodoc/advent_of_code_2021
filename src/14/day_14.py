from aocd.models import Puzzle
from more_itertools import windowed
from collections import Counter, OrderedDict, defaultdict

def part_a(template: str, rules: dict):
    for _ in range(10):
        i = 1
        for pair in windowed(template, 2):
            template = template[:i] + rules[''.join(pair)] + template[i:]
            i += 2
    most, least = max(set(template), key=template.count), min(set(template), key=template.count)
    return template.count(most) - template.count(least)

def part_b(template: str, rules: dict):
    pass

def load(data: str):
    template, rules = data.split('\n\n')
    return template, {rule.split(' -> ')[0]: rule.split(' -> ')[1] for rule in rules.splitlines()}

puzzle = Puzzle(year=2021, day=14)
# ans_a = part_a(*load(puzzle.input_data))
# print(ans_a)
#puzzle.answer_a = ans_a  # 3095

with open('test.in') as f:
    test = f.read()

ans = part_b(*load(test))
print(ans)