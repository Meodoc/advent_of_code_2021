from aocd.models import Puzzle


def part_a(p1_pos: int, p2_pos: int):
    p1_score, p2_score = 0, 0
    det_die = 0

    while True:
        p1_pos, det_die = play_move(p1_pos, det_die, deterministic=True)
        p1_score += p1_pos
        if p1_score >= 1000:
            break

        p2_pos, det_die = play_move(p2_pos, det_die, deterministic=True)
        p2_score += p2_pos
        if p2_score >= 1000:
            break

    return p1_score * det_die if p2_score >= 1000 else p2_score * det_die


def play_move(pos: int, die: int, deterministic: bool):
    if deterministic:
        for _ in range(3):
            die += 1
            pos = (pos + die) % 10 if (pos + die) % 10 != 0 else 10
        return pos, die



def load(data: str):
    p1_start, p2_start = data.splitlines()
    p1_start = p1_start.split(':')[1].strip()
    p2_start = p2_start.split(':')[1].strip()
    return int(p1_start), int(p2_start)


puzzle = Puzzle(year=2021, day=21)
ans_a = part_a(*load(puzzle.input_data))
print(ans_a)
# puzzle.answer_a = ans_a  # 711480

with open('test.in', 'r') as f:
    test = f.read()
#
# ans = part_a(*load(test))
# print(ans)