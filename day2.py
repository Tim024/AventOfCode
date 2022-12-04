from utils import read_data

LINES = read_data(2, example=False)
TYPE = {'A': 'ROCK', 'B': 'PAPER', 'C': 'SCISSORS'}
VALUES = {v: k for k, v in TYPE.items()}
SCORES = {'ROCK': 1, 'PAPER': 2, 'SCISSORS': 3}
GAME_SCORES = {'L': 0, 'W': 6, 'D': 3}
WINNING_TYPE = {'ROCK': 'PAPER', 'PAPER': 'SCISSORS', 'SCISSORS': 'ROCK'}
LOOSING_TYPE = {'ROCK': 'SCISSORS', 'PAPER': 'ROCK', 'SCISSORS': 'PAPER'}


def get_score_p1(ennemy_play, my_play):
    gamestate = 'L'
    if TYPE[ennemy_play] == TYPE[my_play]:
        gamestate = 'D'
    elif TYPE[ennemy_play] == 'ROCK' and TYPE[my_play] == 'PAPER':
        gamestate = 'W'
    elif TYPE[ennemy_play] == 'PAPER' and TYPE[my_play] == 'SCISSORS':
        gamestate = 'W'
    elif TYPE[ennemy_play] == 'SCISSORS' and TYPE[my_play] == 'ROCK':
        gamestate = 'W'
    score = SCORES[TYPE[my_play]] + GAME_SCORES[gamestate]
    print(f"Play: {ennemy_play} ({TYPE[ennemy_play]}) My play: {my_play} ({TYPE[my_play]}) Score: {score} ({gamestate})")
    return score


def get_score_p2(ennemy_play, outcome):
    if outcome == 'X':
        # Should loose
        return get_score_p1(ennemy_play, VALUES[LOOSING_TYPE[TYPE[ennemy_play]]])
    elif outcome == 'Y':
        # Should draw
        return get_score_p1(ennemy_play, ennemy_play)
    elif outcome == 'Z':
        # Should win
        return get_score_p1(ennemy_play, VALUES[WINNING_TYPE[TYPE[ennemy_play]]])


if __name__ == '__main__':
    all_scores = []
    for line in LINES:
        play = line.split(' ')[0]
        my_play = line.split(' ')[1]
        s = get_score_p2(play, my_play)
        all_scores.append(s)
    print(f'Total score: {sum(all_scores)}')
