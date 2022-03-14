from aocd.models import Puzzle
from dataclasses import dataclass

DIGIT_MAPPINGS = {0: {'a', 'b', 'c', 'e', 'f', 'g'},
                  1: {'c', 'f'},
                  2: {'a', 'c', 'd', 'e', 'g'},
                  3: {'a', 'c', 'd', 'f', 'g'},
                  4: {'b', 'c', 'd', 'f'},
                  5: {'a', 'b', 'd', 'f', 'g'},
                  6: {'a', 'b', 'd', 'e', 'f', 'g'},
                  7: {'a', 'c', 'f'},
                  8: {'a', 'b', 'c', 'd', 'e', 'f', 'g'},
                  9: {'a', 'b', 'c', 'd', 'f', 'g'}}

SEGMENT_MAPPINGS = {frozenset({'a', 'b', 'c', 'e', 'f', 'g'}): 0,
                    frozenset({'c', 'f'}): 1,
                    frozenset({'a', 'c', 'd', 'e', 'g'}): 2,
                    frozenset({'a', 'c', 'd', 'f', 'g'}): 3,
                    frozenset({'b', 'c', 'd', 'f'}): 4,
                    frozenset({'a', 'b', 'd', 'f', 'g'}): 5,
                    frozenset({'a', 'b', 'd', 'e', 'f', 'g'}): 6,
                    frozenset({'a', 'c', 'f'}): 7,
                    frozenset({'a', 'b', 'c', 'd', 'e', 'f', 'g'}): 8,
                    frozenset({'a', 'b', 'c', 'd', 'f', 'g'}): 9}


@dataclass
class Entry:
    patterns: list
    outputs: list


def part_a(entries: list):
    unique = 0
    for entry in entries:
        for output in entry.outputs:
            if len(output) in (2, 4, 3, 7):
                unique += 1
    return unique


def part_b(entries: list):
    total = 0

    for entry in entries:
        mapping = decode_mapping(entry.patterns)

        output = 0
        mul = 1000
        for digit in entry.outputs:
            mapped = frozenset(mapping[segment] for segment in digit)
            output += SEGMENT_MAPPINGS[mapped] * mul
            mul //= 10
        total += output

    return total


def decode_mapping(patterns: list):
    def try_decode(mapping_: dict, pattern_: set, digit_: int):
        target = DIGIT_MAPPINGS[digit_]

        # improve existing mappings
        for k, v in mapping_.copy().items():
            match = k & pattern_
            if len(match) == 0:  # no match found, continue
                continue
            if len(match) < len(k):  # found new insight
                mapping_[match] = mapping_[k] & target
                rest = k - match
                if len(rest) > 0:
                    mapping_[rest] = mapping_[k] - (mapping_[k] & target)
                del mapping_[k]
            # remove already handled segments from pattern and target
            pattern_ = pattern_ - match
            if len(mapping_[match] & target) < len(mapping_[match]):  # impossible assignment -> try next digit
                return False
            else:
                target = target - mapping_[match]

        # create new mapping with remaining elements
        if len(pattern_) > 0:
            mapping_[pattern_] = target
        return mapping_

    mapping = dict()

    # handle unique patterns first
    unique = sorted([pattern for pattern in patterns if len(pattern) in (2, 3, 4)], key=len)
    mapping[unique[0]] = {'c', 'f'}  # 1
    mapping[unique[1] - (unique[0] & unique[1])] = {'a'}  # 7
    mapping[unique[2] - (unique[0] & unique[2])] = {'b', 'd'}  # 4

    # figure out rest of mappings
    patterns = [pattern for pattern in patterns if pattern not in unique]
    for pattern in patterns:
        if len(pattern) == 5:
            for digit in (2, 3, 5):
                if (new_mapping := try_decode(mapping.copy(), pattern, digit)) is not False:
                    mapping = new_mapping
                    break
        if len(pattern) == 6:
            for digit in (0, 6, 9):
                if (new_mapping := try_decode(mapping.copy(), pattern, digit)) is not False:
                    mapping = new_mapping
                    break

    # unpack the single value sets
    return {next(iter(k)): next(iter(v)) for k, v in mapping.items()}


def load(data: str):
    entries = []
    for entry in data.splitlines():
        patterns, outputs = entry.split(' | ')
        patterns = [frozenset(pattern) for pattern in patterns.split()]
        outputs = [set(output) for output in outputs.split()]
        entries.append(Entry(patterns, outputs))
    return entries


puzzle = Puzzle(year=2021, day=8)
ans_a = part_a(load(puzzle.input_data))
print(ans_a)
# puzzle.answer_a = ans_a  # 375

ans_b = part_b(load(puzzle.input_data))
print(ans_b)
# puzzle.answer_b = ans_b  # 1019355
