from aocd.models import Puzzle
from dataclasses import dataclass
from collections import defaultdict
from copy import deepcopy

TOTAL_SEGMENTS = 7
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
        mult = 1000
        for digit in entry.outputs:
            mapped = frozenset({list(mapping[frozenset(segment)])[0] for segment in digit})
            output += SEGMENT_MAPPINGS[mapped] * mult
            mult /= 10

        total += output

    return int(total)


def decode_mapping(patterns: list):
    def try_decode(mapping_: dict, pattern_: set, try__: int):
        target = DIGIT_MAPPINGS[try__]

        # improve existing mappings
        for k, v in mapping_.copy().items():
            match = k & pattern_
            if len(match) == 0:  # no match found, continue
                continue
            if len(match) < len(k):  # found new insight
                mapping_[match] = mapping_[k] & target
                rest = k - match
                mapping_[rest] = mapping_[k] - (mapping_[k] & target)
                del mapping_[k]
            pattern_ = pattern_ - match
            if len(mapping_[match] & target) < len(mapping_[match]):
                return False
            else:
                target = target - mapping_[match]

        # create new mapping with remaining elements
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
            for try_ in (2, 3, 5):
                if (new_mapping := try_decode(mapping.copy(), pattern, try_)) is not False:
                    mapping = new_mapping
                    break
        if len(pattern) == 6:
            for try_ in (0, 6, 9):
                if (new_mapping := try_decode(mapping.copy(), pattern, try_)) is not False:
                    mapping = new_mapping
                    break

    return mapping


def old_2_decode_mapping(patterns: list):
    mapping = dict()

    # handle unique patterns first
    unique = sorted([pattern for pattern in patterns if len(pattern) in (2, 3, 7)])

    for segment in unique[0]:  # 1
        mapping[segment] = {'c', 'f'}

    mapping[unique[1] - (unique[0] & unique[1])] = 'a'

    for segment in unique[2] - (unique[0] & unique[2]):
        mapping[segment] = {'b', 'd'}

    # figure out rest of mappings
    patterns.remove(unique)
    for pattern in patterns:
        if len(pattern) == 5:
            for try_ in (2, 3, 5):

                for segment in pattern:
                    if len(mapping[segment]) == 1:
                        pattern.remove(mapping[segment])
                while True:
                    found = False
                    for segment in pattern:
                        if len(mapping[segment] & pattern) == 1:
                            found = True
                            mapping[segment] = mapping[segment] & pattern
                            pattern.remove(mapping[segment])
                    if not found:
                        break
                for segment in pattern:
                    if segment in mapping:
                        mapping[segment] = mapping[segment] & pattern

    for pattern in sorted(patterns):
        if len(pattern) == 2:
            for segment in pattern:
                mapping[segment] = {'c', 'f'}
        elif len(pattern) == 4:
            mapping['a'] = 'blaaa'
        elif len(pattern) == 3:
            for segment in pattern:
                mapping[segment] = {'a', 'c', 'f'}
        # elif len(pattern) == 7:
        #     for segment in pattern:
        #         mapping[segment] = {'a', 'b', 'c', 'd', 'e', 'f', 'g'}

    # resolve rest of mappings
    for pattern in patterns:
        if len(pattern) == 5:
            pass

        if len(pattern) == 6:
            pass

    pass


def old_decode_mapping(patterns: list):
    def handle_distinct_mapping(segment_: str):
        try:
            elem = possible_mappings[segment_].pop()
        except KeyError:
            return False

        found_ = True

        possible_mappings.pop(segment_)
        mapping[segment_] = elem
        new_distinct = []
        for k, v in possible_mappings.items():
            possible_mappings[k].discard(elem)
            if len(possible_mappings[k]) == 1:
                new_distinct.append(k)
        for n in new_distinct:
            found_ = found_ & handle_distinct_mapping(n)

        return found_

    unmapped = {'a', 'b', 'c', 'd', 'e', 'f', 'g'}
    possible_mappings = {'a': unmapped, 'b': unmapped, 'c': unmapped, 'd': unmapped, 'e': unmapped, 'f': unmapped,
                         'g': unmapped}
    mapping = dict()

    for pattern in patterns:
        if len(pattern) == 2:  # digit 1
            for segment in pattern:
                if segment in possible_mappings.keys():
                    possible_mappings[segment] = possible_mappings[segment] & DIGIT_MAPPINGS[1]
                    if len(possible_mappings[segment]) == 1:
                        handle_distinct_mapping(segment)
        elif len(pattern) == 3:  # digit 7
            for segment in pattern:
                if segment in possible_mappings.keys():
                    possible_mappings[segment] = possible_mappings[segment] & DIGIT_MAPPINGS[7]
                    if len(possible_mappings[segment]) == 1:
                        handle_distinct_mapping(segment)
        elif len(pattern) == 4:  # digit 4
            for segment in pattern:
                if segment in possible_mappings.keys():
                    possible_mappings[segment] = possible_mappings[segment] & DIGIT_MAPPINGS[4]
                    if len(possible_mappings[segment]) == 1:
                        handle_distinct_mapping(segment)
        elif len(pattern) == 7:  # digit 8
            for segment in pattern:
                if segment in possible_mappings.keys():
                    possible_mappings[segment] = possible_mappings[segment] & DIGIT_MAPPINGS[8]
                    if len(possible_mappings[segment]) == 1:
                        handle_distinct_mapping(segment)
        elif len(pattern) == 5:  # digit 2, 3, 5
            for digit in (2, 3, 5):
                found = False
                possible_mappings_backup = deepcopy(possible_mappings)
                mapping_backup = deepcopy(mapping)

                for segment in pattern:
                    if segment in possible_mappings.keys():
                        possible_mappings[segment] = possible_mappings[segment] & DIGIT_MAPPINGS[digit]
                        if len(possible_mappings[segment]) == 1:
                            if handle_distinct_mapping(segment):
                                found = True
                if found:
                    break
                else:
                    possible_mappings = possible_mappings_backup
                    mapping = mapping_backup

                # update_mapping(segment, [2, 3, 5])
                # mapping[segment] = mapping[segment] & (DIGIT_MAPPINGS[2] | DIGIT_MAPPINGS[3] | DIGIT_MAPPINGS[5])
        elif len(pattern) == 6:  # digit 0, 6, 9
            for digit in (0, 6, 9):
                found = False
                possible_mappings_backup = deepcopy(possible_mappings)
                mapping_backup = deepcopy(mapping)
                for segment in pattern:
                    if segment in possible_mappings.keys():
                        possible_mappings[segment] = possible_mappings[segment] & DIGIT_MAPPINGS[digit]
                        if len(possible_mappings[segment]) == 1:
                            if handle_distinct_mapping(segment):
                                found = True
                if found:
                    break
                else:
                    possible_mappings = possible_mappings_backup
                    mapping = mapping_backup
                # mapping[segment] = mapping[segment] & (DIGIT_MAPPINGS[6] | DIGIT_MAPPINGS[9])
        else:
            raise Exception('Invalid pattern length')

    return mapping


def old_2_decode_mapping(patterns: list):
    def handle_distinct_mapping(segment_: str):
        try:
            elem = possible_mappings[segment_].pop()
        except KeyError:
            return False

        found_ = True

        possible_mappings.pop(segment_)
        mapping[segment_] = elem
        new_distinct = []
        for k, v in possible_mappings.items():
            possible_mappings[k].discard(elem)
            if len(possible_mappings[k]) == 1:
                new_distinct.append(k)
        for n in new_distinct:
            found_ = found_ & handle_distinct_mapping(n)

        return found_

    unmapped = {'a', 'b', 'c', 'd', 'e', 'f', 'g'}
    possible_mappings = {'a': unmapped, 'b': unmapped, 'c': unmapped, 'd': unmapped, 'e': unmapped, 'f': unmapped,
                         'g': unmapped}
    mapping = dict()

    for pattern in patterns:
        if len(pattern) == 2:  # digit 1
            for segment in pattern:
                if segment in possible_mappings.keys():
                    possible_mappings[segment] = possible_mappings[segment] & DIGIT_MAPPINGS[1]
                    if len(possible_mappings[segment]) == 1:
                        handle_distinct_mapping(segment)
        elif len(pattern) == 3:  # digit 7
            for segment in pattern:
                if segment in possible_mappings.keys():
                    possible_mappings[segment] = possible_mappings[segment] & DIGIT_MAPPINGS[7]
                    if len(possible_mappings[segment]) == 1:
                        handle_distinct_mapping(segment)
        elif len(pattern) == 4:  # digit 4
            for segment in pattern:
                if segment in possible_mappings.keys():
                    possible_mappings[segment] = possible_mappings[segment] & DIGIT_MAPPINGS[4]
                    if len(possible_mappings[segment]) == 1:
                        handle_distinct_mapping(segment)
        elif len(pattern) == 7:  # digit 8
            for segment in pattern:
                if segment in possible_mappings.keys():
                    possible_mappings[segment] = possible_mappings[segment] & DIGIT_MAPPINGS[8]
                    if len(possible_mappings[segment]) == 1:
                        handle_distinct_mapping(segment)
        elif len(pattern) == 5:  # digit 2, 3, 5
            for digit in (2, 3, 5):
                found = False
                possible_mappings_backup = deepcopy(possible_mappings)
                mapping_backup = deepcopy(mapping)

                for segment in pattern:
                    if segment in possible_mappings.keys():
                        possible_mappings[segment] = possible_mappings[segment] & DIGIT_MAPPINGS[digit]
                        if len(possible_mappings[segment]) == 1:
                            if handle_distinct_mapping(segment):
                                found = True
                if found:
                    break
                else:
                    possible_mappings = possible_mappings_backup
                    mapping = mapping_backup

                # update_mapping(segment, [2, 3, 5])
                # mapping[segment] = mapping[segment] & (DIGIT_MAPPINGS[2] | DIGIT_MAPPINGS[3] | DIGIT_MAPPINGS[5])
        elif len(pattern) == 6:  # digit 0, 6, 9
            for digit in (0, 6, 9):
                found = False
                possible_mappings_backup = deepcopy(possible_mappings)
                mapping_backup = deepcopy(mapping)
                for segment in pattern:
                    if segment in possible_mappings.keys():
                        possible_mappings[segment] = possible_mappings[segment] & DIGIT_MAPPINGS[digit]
                        if len(possible_mappings[segment]) == 1:
                            if handle_distinct_mapping(segment):
                                found = True
                if found:
                    break
                else:
                    possible_mappings = possible_mappings_backup
                    mapping = mapping_backup
                # mapping[segment] = mapping[segment] & (DIGIT_MAPPINGS[6] | DIGIT_MAPPINGS[9])
        else:
            raise Exception('Invalid pattern length')

    return mapping


def old_decode_mapping(patterns: list):
    def update_mapping(segment_: str, digits: list):
        if len(mapping[segment_]) == 1:
            return
        for digit_ in digits:
            mapping[segment_] = mapping[segment] & DIGIT_MAPPINGS[digit_]
            if len(mapping[segment_]) == 1:
                elem = list(mapping[segment_])[0]
                if elem in unmapped:
                    unmapped.remove(elem)
                    for k, v in mapping.items():
                        mapping[k].discard(elem)
                    continue

    unmapped = {'a', 'b', 'c', 'd', 'e', 'f', 'g'}
    mapping = defaultdict(lambda: unmapped)
    # while len(mapping) < TOTAL_SEMENTS:
    for _ in range(10):
        for pattern in patterns:
            if len(pattern) == 2:  # digit 1
                for segment in pattern:
                    update_mapping(segment, [1])
            elif len(pattern) == 3:  # digit 7
                for segment in pattern:
                    update_mapping(segment, [7])
            elif len(pattern) == 4:  # digit 4
                for segment in pattern:
                    update_mapping(segment, [4])
            elif len(pattern) == 7:  # digit 8
                for segment in pattern:
                    update_mapping(segment, [8])
            elif len(pattern) == 5:  # digit 2, 3, 5
                for segment in pattern:
                    update_mapping(segment, [2, 3, 5])
                    # mapping[segment] = mapping[segment] & (DIGIT_MAPPINGS[2] | DIGIT_MAPPINGS[3] | DIGIT_MAPPINGS[5])
            elif len(pattern) == 6:  # digit 6, 9
                for segment in pattern:
                    update_mapping(segment, [6, 9])
                    # mapping[segment] = mapping[segment] & (DIGIT_MAPPINGS[6] | DIGIT_MAPPINGS[9])
            else:
                raise Exception('Invalid pattern length')
    pass


def load(data: str):
    entries = []
    for entry in data.splitlines():
        patterns, outputs = entry.split('|')
        patterns = [frozenset(pattern) for pattern in patterns.rstrip().split()]
        outputs = [set(output) for output in outputs.lstrip().split()]
        entries.append(Entry(patterns, outputs))
    return entries


puzzle = Puzzle(year=2021, day=8)
# ans_a = part_a(load(puzzle.input_data))
# print(ans_a)
# puzzle.answer_a = ans_a  # 375

ans_b = part_b(load(puzzle.input_data))
print(ans_b)
puzzle.answer_b = ans_b  # 1019355


# with open('test.in', 'r') as f:
#     test = f.read()
#
# ans = part_b(load(test))
# print(ans)
