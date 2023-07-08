import random

from language_helpers import check_language
from pause import pause
from player import Player


# -- adding player object --
def add_player(player, list_names_of_bots, game_players, language):
    if player not in list_names_of_bots:
        player_object = Player(player)
        game_players.append(player_object)
        return game_players
    else:
        check_language(language, "Name taken, please choose another username.",
                       "Името е заето, моля изберете друго име.")
        human = add_player(input(), list_names_of_bots, game_players, language)
        return human


# -- choosing number of bots and creates list of players with human player --
def create_list_of_players(number_of_bots, list_names_of_bots, game_players, language):
    if number_of_bots.isdigit():
        if 0 < int(number_of_bots) <= 10:
            for j in range(int(number_of_bots)):
                c = list_names_of_bots[random.randint(0, len(list_names_of_bots) - 1)]
                list_names_of_bots.remove(c)
                add_player(c, list_names_of_bots, game_players, language)
            return int(number_of_bots)
        else:
            check_language(language,
                           "Incorrect input. Please type just one number for opponents between 1 and 10.",
                           "Грешна стойност. Моля напишете само едно число за брой противници в интервала от 1 до 10.")
            create_list_of_players(input(), list_names_of_bots, game_players, language)
    else:
        check_language(language, "Incorrect input. Please type just one number for opponents between 1 and 10.",
                       "Грешна стойност. Моля напишете само едно число за брой противници в интервала от 1 до 10.")
        create_list_of_players(input(), list_names_of_bots, game_players, language)


# -- rotate players --
def next_turn(players):
    players.append(players.popleft())


#  -- get names of the players --
def get_players_name(players):
    return [p.name for p in players]


# -- adds how many times player place a bet to self, helps to place bluffs according to temper --
def add_turns_to_player(player, players):
    current_player = get_player_by_name(player, players)
    current_player.turns += 1


# -- show inactive player if any --
def players_active(players, game_players_names, language):
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
        check_language(language, f'Player {inactive_names[0]} left the game.',
                       f'Играч {inactive_names[0]} напусна играта.')
        pause()
        return players_names
    else:
        return players_names


#  -- check which player lose a die
def check_who_lose_die(c_bidder, l_bidder, players_turns, last_bet, g_players, g_players_names, wild, language):
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
        check_language(language,
                       f'There are {number_of_dices_of_searched_number} numbers of {searched_number} dices. {l_bidder} lose a dice.',
                       f'Има {number_of_dices_of_searched_number} броя зарове със стойност {searched_number}. {l_bidder} губи зарче.')
        pause()
        remove_dice(g_players, l_bidder)
        g_players_names = players_active(g_players, g_players_names, language)
        choosing_player_to_start(l_bidder, g_players, g_players_names)
    else:
        check_language(language,
                       f'There are {number_of_dices_of_searched_number} numbers of {searched_number} dices. {l_bidder} lose a dice.',
                       f'Има {number_of_dices_of_searched_number} броя зарове със стойност {searched_number}. {l_bidder} губи зарче.')
        pause()
        remove_dice(g_players, c_bidder)
        g_players_names = players_active(g_players, g_players_names, language)
        choosing_player_to_start(c_bidder, g_players, g_players_names)
    return g_players_names


#  -- choose player with dice to start round --
def choosing_player_to_start(player, games_players, players_names):
    if len(players_names) > 1:
        while player != games_players[0].name:
            next_turn(games_players)
        if games_players[0].dice == 0:
            next_turn(games_players)


#  -- get the next bidder with dice from players --
def get_next_bidder(all_game_players):
    for i in range(len(all_game_players)):
        if all_game_players[i + 1].dice != 0:
            next_index = (i + 1) % len(all_game_players)
            return all_game_players[next_index]


#  -- check if there is a call from player and no such face dice in hand --
def check_if_players_are_bluffing(players, wild):
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
def print_if_liar(current_player, last_player, player_turn, language):
    check_language(language, f'{current_player} called {last_player} a liar. Everyone showing their dice.', f'{current_player} нарече {last_player} лъжец. Всички играчи показват заровете си.')
    pause(2)
    showing_string = ''
    for pln, d in player_turn.items():
        showing_string += pln
        word = check_language(language, ' has ', ' има ')
        showing_string += word
        showing_string += ', '.join(map(str, d))
        showing_string += ' ; '
    print(f'{showing_string[:-2]}')
    pause(2)


#  -- get player by name if name is a string, not object --
def get_player_by_name(player_name, players):
    for pl in players:
        if pl.name == player_name:
            return pl


#  -- remove dice from player --
def remove_dice(game_player, loser):
    player = get_player_by_name(loser, game_player)
    if player.dice > 0:
        player.dice -= 1
