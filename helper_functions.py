import random
from collections import deque

from stats_memory_players import load_stat, load_initial_memory


#  -- roll dice when starting new round --
def roll_dice(players: deque, g_round: int) -> dict:
    g_round += 1
    players_turns = {}
    for player in players:
        player.clear_stat()
        player.clear_memory()
        player.clear_dice_stat_profile_for_opponents()
        if player.dice > 0:
            cells = []
            for cell in range(player.dice):
                dice_number = random.randint(1, 6)
                cells.append(dice_number)
            players_turns[player.name] = sorted(cells)
            load_stat(player, cells)
            load_initial_memory(player, cells)
    return players_turns


# -- the sum of all dices on the table --
def check_sum_dice(players: deque) -> int:
    return sum([player.dice for player in players])


# -- print text according to game language --
def choose_language(english_language: bool, english: str, bulgarian: str) -> None:
    if english_language:
        print(english)
    else:
        print(bulgarian)
