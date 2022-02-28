from aocd.models import Puzzle
from collections import defaultdict


def part_a(p1_pos: int, p2_pos: int):
    p1_score, p2_score = 0, 0
    det_die = 0

    while True:
        # player 1
        for _ in range(3):
            det_die += 1
            p1_pos = play_move(p1_pos, det_die)
        p1_score += p1_pos
        if p1_score >= 1000:
            break

        # player 2
        for _ in range(3):
            det_die += 1
            p2_pos = play_move(p2_pos, det_die)
        p2_score += p2_pos
        if p2_score >= 1000:
            break

    return p1_score * det_die if p2_score >= 1000 else p2_score * det_die


def part_b(p1_pos: int, p2_pos: int):
    p1_win_cnt, p2_win_cnt = 0, 0
    dirac_die_comb = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}
    # game state: ((p1 pos, p1 score), (p2 pos, p2 score))
    game_states = defaultdict(int, {((p1_pos, 0), (p2_pos, 0)): 1})

    while True:
        # player 1
        prev_game_states = game_states.copy()
        game_states = defaultdict(int)
        for game_state, amount in prev_game_states.items():
            p1, p2 = game_state

            for roll, times in dirac_die_comb.items():
                p1_pos, p1_score = p1
                p1_pos = play_move(p1_pos, roll)
                p1_score += p1_pos
                if p1_score >= 21:
                    p1_win_cnt += (amount * times)
                else:
                    new_game_state = ((p1_pos, p1_score), p2)
                    game_states[new_game_state] += (amount * times)

        print(len(game_states))

        # player 2
        prev_game_states = game_states.copy()
        game_states = defaultdict(int)
        for game_state, amount in prev_game_states.items():
            p1, p2 = game_state

            for roll, times in dirac_die_comb.items():
                p2_pos, p2_score = p2
                p2_pos = play_move(p2_pos, roll)
                p2_score += p2_pos
                if p2_score >= 21:
                    p2_win_cnt += (amount * times)
                else:
                    new_game_state = (p1, (p2_pos, p2_score))
                    game_states[new_game_state] += (amount * times)

        if len(game_states) == 0:
            break

        print(len(game_states))

    print(p1_win_cnt, p2_win_cnt)
    return max(p1_win_cnt, p2_win_cnt)


def play_move(pos: int, die: int):
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

ans_b = part_b(*load(puzzle.input_data))
print(ans_b)
# puzzle.answer_b = ans_b  # 265845890886828


