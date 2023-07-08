import random

from language_helpers import check_language
from stats_memory_players import load_stat, load_initial_memory


# -- choose human action - bet or liar --
def choose_action(string, language):
    if string.lower() == 'b':
        return 'bet'
    elif string.lower() == 'l':
        return 'liar'
    else:
        check_language(language, "Please make a valid choice! Type 'b' or 'l'. ", "Моля направете валиден избор! "
                                                                                  "Напишете 'b' или 'l'. ")
        new_human_string = input().strip()
        human_action = choose_action(new_human_string, language)
        return human_action


# -- check answer if human wants to play again with the same players--
def check_answer(human_answer, language):
    if human_answer.lower() == 'y':
        game_active = True
        return game_active
    elif human_answer.lower() == 'n':
        game_active = False
        return game_active
    else:
        check_language(language, "Please make your choice by pressing 'y' or 'n' button on your keyboard!", "Моля "
                                                                                                            "направете избор като натиснете 'y' или 'n' бутона на клавиатурата си!")
        new_human_answer = input().strip()
        check_answer(new_human_answer, language)


#  -- human choice for game mode regular/normal or advanced/wild ones --
def choose_game_mode(human_answer, language):
    if human_answer.lower() == 'w':
        w_mode = True
        return w_mode
    elif human_answer.lower() == 'n':
        w_mode = False
        return w_mode
    else:
        check_language(language, "Please make your choice by pressing 'w' or 'n' button on your keyboard!", "Моля "
                                                                                                            "направете своя избор като натиснете 'w' или 'n' бутона на клавиатурата си!")
        check_language(language, "By pressing 'w' you will enter advanced wild one's mode. By pressing 'n' you will "
                                 "play a regular game.", "Натискайки 'w' ще задействате режима на лудите единици. "
                                                         "Натискайки 'n' ще играете обикновена игра.")
        new_human_answer = input().strip()
        check_answer(new_human_answer, language)


#  -- roll dice when starting new round --
def roll_dice(players, g_round):
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
def check_sum_dice(players):
    return sum([player.dice for player in players])
