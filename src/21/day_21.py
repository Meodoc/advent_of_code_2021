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


def part_b(p1_pos: int, p2_pos: int):
    pos_q = [(p1_pos, p2_pos)]
    score_q = [(0, 0)]
    dirac_die = (1, 2, 3)

    p1_win_cnt, p2_win_cnt = 0, 0

    while True:
        #print("Player 1 plays:")

        # player 1 plays
        new_pos_q = []
        new_score_q = []
        for i in range(len(pos_q)):
            p1_pos, p2_pos = pos_q[i]
            p1_score, p2_score = score_q[i]
            #print(i, p1_pos, p2_pos)

            new_p1_pos_q = [play_move(p1_pos, roll) for roll in dirac_die]
            new_pos_q.extend((new_p1_pos, p2_pos) for new_p1_pos in new_p1_pos_q)
            new_score_q.extend((p1_score + new_p1_pos, p2_score) for new_p1_pos in new_p1_pos_q)

        pos_q = new_pos_q
        score_q = new_score_q

        assert(len(pos_q) == len(score_q))

        rem_idx = set()
        for i, score in enumerate(score_q):
            p1_score, p2_score = score
            if p1_score >= 21:
                p1_win_cnt += 1
                rem_idx.add(i)
            elif p2_score >= 21:
                p2_win_cnt += 1
                rem_idx.add(i)
        pos_q = [pos for i, pos in enumerate(pos_q) if i not in rem_idx]
        score_q = [score for i, score in enumerate(score_q) if i not in rem_idx]

        # for i in rem_idx:
        #     del pos_q[i]
        #     del score_q[i]

        # for pos in pos_q:
        #     print(pos)
        # for score in score_q:
        #     print(score)

        #print("\nPlayer 2 plays:")
        # player 2 plays
        new_pos_q = []
        new_score_q = []
        for i in range(len(pos_q)):
            p1_pos, p2_pos = pos_q[i]
            p1_score, p2_score = score_q[i]
            #print(i, p1_pos, p2_pos)

            new_p2_pos_q = [play_move(p2_pos, roll) for roll in dirac_die]
            new_pos_q.extend((p1_pos, new_p2_pos) for new_p2_pos in new_p2_pos_q)
            new_score_q.extend((p1_score, p2_score + new_p2_pos) for new_p2_pos in new_p2_pos_q)

        pos_q = new_pos_q
        score_q = new_score_q

        rem_idx = set()
        for i, score in enumerate(score_q):
            p1_score, p2_score = score
            if p1_score >= 21:
                p1_win_cnt += 1
                rem_idx.add(i)
            elif p2_score >= 21:
                p2_win_cnt += 1
                rem_idx.add(i)

        pos_q = [pos for i, pos in enumerate(pos_q) if i not in rem_idx]
        score_q = [score for i, score in enumerate(score_q) if i not in rem_idx]
        # for i in rem_idx:
        #     del pos_q[i]
        #     del score_q[i]

        # for pos in pos_q:
        #     print(pos)
        # for score in score_q:
        #     print(score)

        if len(pos_q) == 0:
            break

    return p1_win_cnt, p2_win_cnt


def play_move(pos: int, die: int, deterministic: bool = False):
    if deterministic:
        for _ in range(3):
            die += 1
            pos = (pos + die) % 10 if (pos + die) % 10 != 0 else 10
        return pos, die

    return (pos + die) % 10 if (pos + die) % 10 != 0 else 10

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

ans = part_b(*load(test))
print(ans)