import random
from collections import deque

from pause import pause
from player import Player
from print import Print
from stats_memory_players import get_player_by_name
from text_instructions import text_left_game, \
    text_result_and_who_lose_die, text_someone_call_other_liar


# -- adding player object --
def add_player(player: str, list_names_of_bots: list, game_players: deque, language: bool) -> deque:
    if player not in list_names_of_bots:
        player_object = Player(player)
        game_players.append(player_object)
        return game_players
    else:
        Print.text_choose_name_again()
        human = add_player(input(), list_names_of_bots, game_players, language)
        return human


# -- choosing number of bots and creates list of players with human player --
def create_list_of_players(number_of_bots: str, list_names_of_bots: list, game_players: deque, language: bool) -> int:
    if number_of_bots.isdigit():
        if 0 < int(number_of_bots) <= 10:
            for j in range(int(number_of_bots)):
                c = list_names_of_bots[random.randint(0, len(list_names_of_bots) - 1)]
                list_names_of_bots.remove(c)
                add_player(c, list_names_of_bots, game_players, language)
            return int(number_of_bots)
        else:
            Print.text_incorrect_input_opponents()
            create_list_of_players(input(), list_names_of_bots, game_players, language)
    else:

        Print.text_incorrect_input_opponents()
        create_list_of_players(input(), list_names_of_bots, game_players, language)


# -- rotate players --
def next_turn(players: deque) -> None:
    players.append(players.popleft())


#  -- get names of the players --
def get_players_name(players: deque) -> list:
    return [p.name for p in players]


# -- adds how many times player place a bet to self, helps to place bluffs according to temper --
def add_turns_to_player(player: Player, players: deque) -> None:
    current_player = get_player_by_name(player, players)
    current_player.turns += 1


# -- show inactive player if any --
def players_active(players: deque, game_players_names: list, language: bool) -> list:
    game_players_names = game_players_names
    players_names = []
    inactive_names = []
    for player in players:
        if player.name in game_players_names:
            if player.dice == 0:
                inactive_names.append(player.name)
            else:
                players_names.append(player.name)
    if inactive_names:
        text_left_game(language, inactive_names)
        return players_names
    else:
        return players_names


#  -- check which player lose a die
def check_who_lose_die(c_bidder: Player, l_bidder: Player, players_turns: dict, last_bet: list, g_players: deque,
                       g_players_names: list, wild: bool, language: bool) -> list:
    searched_number = int(last_bet[1])
    number_of_dices_of_searched_number = 0
    for k, v in players_turns.items():
        for i in range(len(v)):
            if wild:
                if v[i] == searched_number or v[i] == 1:
                    number_of_dices_of_searched_number += 1
            else:
                if v[i] == searched_number:
                    number_of_dices_of_searched_number += 1
    if number_of_dices_of_searched_number < int(last_bet[0]):
        text_result_and_who_lose_die(language, number_of_dices_of_searched_number, searched_number, l_bidder)
        remove_dice(g_players, l_bidder)
        g_players_names = players_active(g_players, g_players_names, language)
        choosing_player_to_start(l_bidder, g_players, g_players_names)
    else:

        text_result_and_who_lose_die(language, number_of_dices_of_searched_number, searched_number, c_bidder)
        remove_dice(g_players, c_bidder)
        g_players_names = players_active(g_players, g_players_names, language)
        choosing_player_to_start(c_bidder, g_players, g_players_names)
    return g_players_names


#  -- choose player with dice to start round --
def choosing_player_to_start(player: Player, games_players: deque, players_names: list) -> None:
    if len(players_names) > 1:
        while player != games_players[0].name:
            next_turn(games_players)
        if games_players[0].dice == 0:
            next_turn(games_players)


#  -- get the next bidder with dice from players --
def get_next_bidder(all_game_players: deque) -> Player:
    for i in range(len(all_game_players)):
        if all_game_players[i + 1].dice != 0:
            next_index = (i + 1) % len(all_game_players)
            return all_game_players[next_index]


#  -- check if there is a call from player and no such face dice in hand --
def check_if_players_are_bluffing(players: deque, wild: bool) -> None:
    for player in players:
        bluffer = 0
        if player.profile_for_opponents['called_dice'][0] != 0:
            for i in range(1, 7):
                if wild:
                    if (player.profile_for_opponents['called_dice'][1][i] > 0) and (
                            (player.stat[i] == 0) or (player.stat[1] == 0)):
                        bluffer += 1
                else:
                    if (player.profile_for_opponents['called_dice'][1][i] > 0) and (player.stat[i] == 0):
                        bluffer += 1
            if bluffer > 0 and player.dice != 0:
                player.profile_for_opponents['tempers'] += 0
                player.profile_for_opponents['total_calls'] += 1
            elif bluffer <= 0 and player.dice != 0:
                player.profile_for_opponents['tempers'] += 1
                player.profile_for_opponents['total_calls'] += 1
        player.calculate_temper_for_opponents()


#  -- when someone is challenged show dice in players hand --
def print_if_liar(current_player: str, last_player: str, player_turn: dict, language: bool) -> None:
    text_someone_call_other_liar(language, current_player, last_player)
    showing_string = ''
    for pln, d in player_turn.items():
        showing_string += pln
        word = Print.get_verb()
        showing_string += str(word)
        showing_string += ', '.join(map(str, d))
        showing_string += ' ; '
    print(f'{showing_string[:-2]}')
    pause()


#  -- remove dice from player --
def remove_dice(game_players: deque, loser: Player):
    player = get_player_by_name(loser, game_players)
    if player.dice > 0:
        player.dice -= 1
