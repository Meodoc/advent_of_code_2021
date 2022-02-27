from aocd.models import Puzzle
from collections import defaultdict

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
    p1_win_cnt, p2_win_cnt = 0, 0
    dirac_die = (1, 2, 3)
    # game state: ((p1 pos, p1 score), (p2 pos, p2 score))
    game_states = defaultdict(int, {((p1_pos, 0), (p2_pos, 0)): 1})
    print(game_states)

    # 1708190453241
    # 13762205476306
    # 283083829957006
    # 821727078918406
    # 444356092776315

    # 2355241912947
    # 7580058074983
    # 336254685904828
    # 993603941564518
    # 341960390180808


    while True:
        # player 1 plays
        old_game_states = game_states.copy()
        for game_state, amount in old_game_states.items():
            p1, p2 = game_state
            p1_pos, p1_score = p1

            # generate all possible new positions for player 1 when rolling 3 times
            new_p1_pos = [p1_pos]
            for roll in range(3):
                old_pos = new_p1_pos.copy()
                for pos in old_pos:
                    new_p1_pos.extend(play_move(pos, die) for die in dirac_die)
                    new_p1_pos.remove(pos)

            # construct the new game states and add the created amount to the total game states
            for pos in new_p1_pos:
                # if the new game state is winning, add the score and dont add it to the game states
                score = p1_score + pos
                if score >= 21:
                    p1_win_cnt += amount
                else:
                    new_game_state = ((pos, score), p2)
                    game_states[new_game_state] += amount

            # remove the original game state
            del game_states[game_state]

        print(len(game_states))

        # break if all games are finished
        if len(game_states) == 0:
            break

        # player 2 plays
        old_game_states = game_states.copy()
        for game_state, amount in old_game_states.items():
            p1, p2 = game_state
            p2_pos, p2_score = p2

            # generate all possible new positions for player 2 when rolling 3 times
            new_p2_pos = [p2_pos]
            for roll in range(3):
                old_pos = new_p2_pos.copy()
                for pos in old_pos:
                    new_p2_pos.extend(play_move(pos, die) for die in dirac_die)
                    new_p2_pos.remove(pos)

            # construct the new game states and add the created amount to the total game states
            for pos in new_p2_pos:
                # if the new game state is winning, remove it and dont add it to the game states
                score = p2_score + pos
                if score >= 21:
                    p2_win_cnt += amount
                else:
                    new_game_state = (p1, (pos, score))
                    game_states[new_game_state] += amount

            # remove the original game state
            del game_states[game_state]

        print(len(game_states))

        # break if all games are finished
        if len(game_states) == 0:
            break

    print(game_states)
    print(p1_win_cnt, p2_win_cnt)

def old():

    while True:

        # player 1 plays
        new_pos_q = []
        new_score_q = []
        for i in range(len(pos_q)):
            p1_pos, p2_pos = pos_q[i]
            p1_score, p2_score = score_q[i]
            #print(i, p1_pos, p2_pos)

            new_p1_pos_q = play_move(p1_pos, 0)
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

        # for pos in pos_q:
        #     print(pos)
        # for score in score_q:
        #     print(score)

        # player 2 plays
        new_pos_q = []
        new_score_q = []
        for i in range(len(pos_q)):
            p1_pos, p2_pos = pos_q[i]
            p1_score, p2_score = score_q[i]
            #print(i, p1_pos, p2_pos)

            new_p2_pos_q = play_move(p2_pos, 0)
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

    # poss_3_roll_dirac_outcomes = (3, 4, 5, 6, 7, 8, 9)
    # return [(pos + die) % 10 if (pos + die) % 10 != 0 else 10 for die in poss_3_roll_dirac_outcomes]
    return (pos + die) % 10 if (pos + die) % 10 != 0 else 10

def load(data: str):
    p1_start, p2_start = data.splitlines()
    p1_start = p1_start.split(':')[1].strip()
    p2_start = p2_start.split(':')[1].strip()
    return int(p1_start), int(p2_start)


puzzle = Puzzle(year=2021, day=21)
# ans_a = part_a(*load(puzzle.input_data))
# print(ans_a)
# puzzle.answer_a = ans_a  # 711480

with open('test.in', 'r') as f:
    test = f.read()
#
# ans = part_a(*load(test))
# print(ans)

ans = part_b(*load(test))
print(ans)