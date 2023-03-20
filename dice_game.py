import math
import random
import time
from collections import deque


# -- player class to create both human and bot players --
class Player:
    def __init__(self, player_name):
        self.turns = 1
        self.name = player_name
        self.dice = 5
        # according to temper bots place bluffs more or less often
        self.temper = random.uniform(0.25, 1)
        # here are dice in own hand
        self.stat = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        # based on these stats opponents calculate temper of a player
        self.profile_for_opponents = {
            'tempers': 0,
            'total_calls': 0.01,
            'called_dice': [0, {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}]
        }
        # if opponent is trustworthy player adds opponents' dice
        self.memory = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        # here is how opponent bots see temper of the player
        self.temper_for_other_players = 0

    def restore_dice(self):
        self.dice = 5

    def clear_stat(self):
        self.stat = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}

    def clear_memory(self):
        self.memory = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}

    def clear_dice_stat_profile_for_opponents(self):
        self.profile_for_opponents['called_dice'] = [0, {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}]

    def calculate_temper_for_opponents(self):
        self.temper_for_other_players = self.profile_for_opponents['tempers'] / self.profile_for_opponents[
            'total_calls']


# -- adding player object --
def add_player(player):
    if player not in list_names_of_bots:
        player_object = Player(player)
        game_players.append(player_object)
        return game_players
    else:
        print("Name taken, please choose another username.")
        human = add_player(input())
        return human


# -- choosing number of bots and creates list of players with human player --
def create_list_of_players(number_of_bots):
    if number_of_bots.isdigit():
        if 0 < int(number_of_bots) <= 10:
            for j in range(int(number_of_bots)):
                c = list_names_of_bots[random.randint(0, len(list_names_of_bots) - 1)]
                list_names_of_bots.remove(c)
                add_player(c)
            return int(number_of_bots)
        else:
            print("Incorrect input. Please type just one number for opponents between 1 and 10.")
            create_list_of_players(input())
    else:
        print("Incorrect input. Please type just one number for opponents between 1 and 10.")
        create_list_of_players(input())


#  -- initiate time pause --
def pause(a=1.0):
    time.sleep(a)


# -- rotate players --
def next_turn(players):
    players.append(players.popleft())


# -- the sum of all dices on the table --
def check_sum_dice(players):
    return sum([player.dice for player in players])


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


#  -- load dice values when new round starts --
def load_stat(player, data):
    for i in range(len(data)):
        player.stat[data[i]] += 1


#  -- load other players bets to memory if their stat is trustworthy--
def load_memory(current_player, bet, players):
    c_player = get_player_by_name(current_player, players)
    for player in players:
        if current_player != player.name and c_player.temper_for_other_players > 0.55:
            player.memory[int(bet[1])] += 1
        elif current_player == player.name and player.dice != 0:
            player.profile_for_opponents['called_dice'][0] += 1
            player.profile_for_opponents['called_dice'][1][int(bet[1])] += 1


#  -- load self dices to memory --
def load_initial_memory(player, data):
    for i in range(len(data)):
        player.memory[data[i]] += 1


#  -- remove dice from player --
def remove_dice(game_player, loser):
    player = get_player_by_name(loser, game_player)
    if player.dice > 0:
        player.dice -= 1


# -- choose human action - bet or liar --
def choose_action(string):
    if string.lower() == 'b':
        return 'bet'
    elif string.lower() == 'l':
        return 'liar'
    else:
        print(f"Please make a valid choice! Type 'b' or 'l'. ")
        new_human_string = input().strip()
        human_action = choose_action(new_human_string)
        return human_action


# -- adds how many times player place a bet to self, helps to place bluffs according to temper --
def add_turns_to_player(player, players):
    current_player = get_player_by_name(player, players)
    current_player.turns += 1


# -- place bet on table --
def place_bet(current_bet, player_name, players):
    load_memory(player_name, current_bet, players)
    add_turns_to_player(player_name, players)
    print(f'{player_name} bet for at least {current_bet[0]} dice with face number {current_bet[1]}.')
    pause()
    previous_bet = current_bet
    liar_statement = False
    return [liar_statement, previous_bet]


# -- validate bets --
def valid_bet(current_bet, previous_bet, sum_of_dice):
    if len(current_bet) != 2:
        return False
    elif not (str(current_bet[0]).isdigit() and str(current_bet[1]).isdigit()):
        return False
    else:
        if previous_bet == ['0', '0']:
            if (1 <= int(current_bet[0]) <= sum_of_dice) and (1 <= int(current_bet[1]) <= 6):
                return True
            else:
                return False
        else:
            if (sum_of_dice >= int(current_bet[0]) > int(previous_bet[0]) and (
                    int(previous_bet[1]) == int(current_bet[1]))) \
                    or ((1 <= int(previous_bet[0]) <= sum_of_dice) and int(current_bet[1]) > int(previous_bet[1])):
                return True
            else:
                return False


#  -- get player by name if name is a string, not object --
def get_player_by_name(player_name, players):
    for pl in players:
        if pl.name == player_name:
            return pl


#  -- according to temper and times player places bet in the round, choose if the bet is bluff or not --
def calc_bet_according_to_temper(last_bet, current_player, last_player, sum_of_dice, players, wild):
    new_bet_to_be_checked = []
    current_player_object = get_player_by_name(current_player, players)
    opponents_chance = 0
    if type(last_player) == str:
        if last_player != '':
            last_player = get_player_by_name(last_player, players)
            opponents_chance = calculate_probability(
                last_bet, sum_of_dice, last_player, wild, keyword='memory')

    if current_player_object.temper <= 0.35:
        if current_player_object.turns % 3 == 0:
            new_bet_to_be_checked = calculate_new_bet(
                last_bet, current_player_object, last_player, sum_of_dice, players, wild, opponents_chance)
        else:
            new_bet_to_be_checked = bluff_bet(
                last_bet, sum_of_dice, current_player_object, last_player, players, wild, opponents_chance)
    elif 0.35 < current_player_object.temper <= 0.55:
        if current_player_object.turns % 2 == 0:
            new_bet_to_be_checked = calculate_new_bet(
                last_bet, current_player_object, last_player, sum_of_dice, players, wild, opponents_chance)
        else:
            new_bet_to_be_checked = bluff_bet(
                last_bet, sum_of_dice, current_player_object, last_player, players, wild, opponents_chance)
    elif 0.55 < current_player_object.temper <= 0.75:
        if current_player_object.turns % 3 == 0:
            new_bet_to_be_checked = bluff_bet(
                last_bet, sum_of_dice, current_player_object, last_player, players, wild, opponents_chance)
        else:
            new_bet_to_be_checked = calculate_new_bet(
                last_bet, current_player_object, last_player, sum_of_dice, players, wild, opponents_chance)
    elif current_player_object.temper > 0.75:
        if current_player_object.turns % 4 == 0:
            new_bet_to_be_checked = bluff_bet(
                last_bet, sum_of_dice, current_player_object, last_player, players, wild, opponents_chance)
        else:
            new_bet_to_be_checked = calculate_new_bet(
                last_bet, current_player_object, last_player, sum_of_dice, players, wild, opponents_chance)
    # --- returning empty bet equal to calling liar ---
    if int(last_bet[0]) >= sum_of_dice:
        new_bet_to_be_checked = []
    elif int(last_bet[1]) != 0:
        if wild:
            if int(last_bet[0]) > \
                    (sum_of_dice - current_player_object.dice) + current_player_object.stat[int(last_bet[1])] + \
                    current_player_object.stat[1]:
                new_bet_to_be_checked = []
        else:
            if int(last_bet[0]) > \
                    (sum_of_dice - current_player_object.dice) + current_player_object.stat[int(last_bet[1])]:
                new_bet_to_be_checked = []

    return new_bet_to_be_checked


# --calculate test new  bet --
def calculate_new_bet(last_bet, player, last_player, sum_of_dice, players, wild, opponents_chance):
    if last_player != '':
        if type(last_player) == str:
            last_player = get_player_by_name(last_player, players)
        neo_bet = []

        if 0 < last_player.temper_for_other_players < 0.55:
            if player.temper < 0.55:
                if 0 < opponents_chance < 0.7:
                    neo_bet = []
                    return neo_bet
            else:
                if 0 < opponents_chance < 0.5:
                    neo_bet = []
                    return neo_bet

        else:
            sum_dice_in_memory, probability_by_memory, new_test_bet = if_not_blank_bet(
                player, last_bet, opponents_chance, sum_of_dice, players, wild, last_player)

            if sum_dice_in_memory < sum_of_dice and probability_by_memory > 0.6:
                neo_bet = new_test_bet
            elif opponents_chance != 0:
                neo_bet = []
            else:
                neo_bet = bluff_bet(last_bet, sum_of_dice, player, last_player, players, wild, opponents_chance)

        if opponents_chance > 0.9 and neo_bet == []:
            neo_bet = bluff_bet(last_bet, sum_of_dice, player, last_player, players, wild, opponents_chance)
        if player.temper < 0.55:
            coefficient = 0.2
            if wild:
                coefficient = 0.3

            if int(last_bet[0]) != 0 and int(last_bet[0]) > sum_of_dice * coefficient:
                return []
        else:
            coefficient = 0.3
            if wild:
                coefficient = 0.45
            if int(last_bet[0]) != 0 and int(last_bet[0]) > sum_of_dice * coefficient:
                return []
        return neo_bet
    else:
        sum_dice_in_memory, probability_by_memory, new_test_bet = if_not_blank_bet(
            player, last_bet, opponents_chance, sum_of_dice, players, wild, last_player)
        return new_test_bet


#  -- if the new bet is not blank(call previous player liar) --
def if_not_blank_bet(player, last_bet, opponents_chance, sum_of_dice, players, wild, last_player):
    if type(player) == str:
        player = get_player_by_name(player, players)
    prev_count, prev_dice = last_bet
    prev_count = int(prev_count)
    prev_dice = int(prev_dice)
    new_test_bet = []
    sum_dice_in_memory = sum(player.memory.values())
    for k, v in player.memory.items():
        if wild:
            if (v > prev_count and k == prev_dice) or (1 <= v <= sum_of_dice and k > prev_dice):
                if (v - prev_count) >= 0 or (player.memory[1] - prev_count) >= 0:
                    v = prev_count + 1
                if valid_bet([v, k], last_bet, sum_of_dice):
                    new_test_bet = [v, k]
                    break
        else:
            if (v > prev_count and k == prev_dice) or (1 <= v <= sum_of_dice and k > prev_dice):
                if (v - prev_count) >= 0:
                    v = prev_count + 1
                if valid_bet([v, k], last_bet, sum_of_dice):
                    new_test_bet = [v, k]
                    break

    probability_by_memory = calculate_probability(last_bet, sum_of_dice, player, wild, 'memory')
    if opponents_chance > 0.6 and len(new_test_bet) == 0:
        new_test_bet = bluff_bet(last_bet, sum_of_dice, player, last_player, players, wild, opponents_chance)
    return [sum_dice_in_memory, probability_by_memory, new_test_bet]


#  -- calculate bluff bet --
def bluff_bet(prev_bet, sum_of_dice, current_player, last_player, players, wild, opponents_chance):
    if type(current_player) == str:
        current_player = get_player_by_name(current_player, players)
    if last_player != '':
        new_bet_to_be_checked = []
        if type(last_player) == str:
            last_player = get_player_by_name(last_player, players)
        if wild:
            if int(prev_bet[0]) > \
                    sum_of_dice - current_player.memory[int(prev_bet[1])] - current_player.memory[1] - last_player.dice:
                new_bet_to_be_checked = []
        else:
            if int(prev_bet[0]) > sum_of_dice - current_player.memory[int(prev_bet[1])] - last_player.dice:
                new_bet_to_be_checked = []
        coefficient = 0.15
        if wild:
            coefficient = 0.25
        if int(prev_bet[0]) > sum_of_dice * coefficient:
            new_bet_to_be_checked = []
        if opponents_chance > 0.9 and new_bet_to_be_checked == []:
            prev_count, prev_dice = prev_bet
            prev_dice = int(prev_dice)
            prev_count = int(prev_count)
            for i in range(900):
                new_count = 0
                new_dice = 0
                rand_num = random.randint(0, 1)
                if rand_num == 0:
                    if wild:
                        rand_count = random.randint(1, 2)
                        new_count = prev_count + rand_count
                    else:
                        new_count = prev_count + 1
                    new_dice = prev_dice
                    if prev_dice == 0:
                        if wild:
                            new_dice = 2
                        else:
                            new_dice = 1
                else:
                    for index in range(sum_of_dice):
                        new_count = random.randint((index + 1), (index + 2))
                        if prev_dice == 6:
                            new_dice = 6
                        elif prev_dice == 0:
                            if wild:
                                prev_dice = 1
                                new_dice = 2
                            else:
                                new_dice = 1
                        else:
                            new_dice = prev_dice + 1
                        new_bet_to_be_checked = [new_count, new_dice]
                        valid_condition = valid_bet(new_bet_to_be_checked, prev_bet, sum_dice)
                        if valid_condition:
                            break
                new_bet_to_be_checked = [new_count, new_dice]
                valid_condition = valid_bet(new_bet_to_be_checked, prev_bet, sum_dice)
                if valid_condition:
                    return new_bet_to_be_checked
            return new_bet_to_be_checked
    prev_count, prev_dice = prev_bet
    prev_dice = int(prev_dice)
    prev_count = int(prev_count)
    for i in range(900):
        new_count = 0
        new_dice = 0
        rand_num = random.randint(0, 1)
        if rand_num == 0:
            new_count = prev_count + random.randint(1, 2)
            new_dice = prev_dice
            if prev_dice == 0:
                if wild:
                    new_dice = 2
                else:
                    new_dice = 1
        else:
            for index in range(1, sum_of_dice):
                if prev_count < 5:
                    new_count = random.randint(index, (index + 2))
                else:
                    new_count = random.randint(index, (index + 1))

                if prev_dice == 6:
                    new_dice = 6
                elif prev_dice == 0:
                    if wild:
                        prev_dice = 1
                        new_dice = 2
                    else:
                        new_dice = 1
                else:
                    new_dice = prev_dice + 1
                new_bet_to_be_checked = [new_count, new_dice]
                valid_condition = valid_bet(new_bet_to_be_checked, prev_bet, sum_dice)
                if valid_condition:
                    break
        new_bet_to_be_checked = [new_count, new_dice]
        valid_condition = valid_bet(new_bet_to_be_checked, prev_bet, sum_dice)
        if valid_condition:
            return new_bet_to_be_checked
    return []


#  -- calculate probability using binomial distribution--
def calculate_probability(bet, sum_of_dice, current_player, wild, keyword='stat'):
    p = 1 / 6
    if wild:
        p = 1 / 3

    own_dice = current_player.dice
    n = sum_of_dice - own_dice
    searched_number = int(bet[1])
    if wild:
        in_my_hand_of_searched_number = current_player.stat[1]
    else:
        in_my_hand_of_searched_number = 0
    if keyword == 'stat':
        for k, v in current_player.stat.items():
            if wild:
                if k == searched_number or k == 1:
                    in_my_hand_of_searched_number += v
            else:
                if k == searched_number:
                    in_my_hand_of_searched_number += v
    else:
        for k, v in current_player.memory.items():
            if wild:
                if k == searched_number or k == 1:
                    in_my_hand_of_searched_number += v
            else:
                if k == searched_number:
                    in_my_hand_of_searched_number += v

    r = int(bet[0]) - in_my_hand_of_searched_number
    if r < 0:
        r = 0
    check_probability_for_bet_or_more = 0
    for i in range(n - r):
        check_probability_for_bet_or_more += math.comb(n, r) * (p ** r) * (1 - p) ** (n - r)
        r += 1

    return check_probability_for_bet_or_more


#  -- get names of the players --
def get_players_name(players):
    return [p.name for p in players]


#  -- when someone is challenged show dice in players hand --
def print_if_liar(current_player, last_player, player_turn):
    print(f'{current_player} called {last_player} a liar. Everyone showing their dice.')
    pause(2)
    showing_string = ''
    for pln, d in player_turn.items():
        showing_string += pln
        showing_string += ' has '
        showing_string += ', '.join(map(str, d))
        showing_string += ' ; '
    print(f'{showing_string[:-2]}')
    pause(2)


# -- show inactive player if any --
def players_active(players, g_players_names):
    g_players_names = g_players_names
    players_names = []
    inactive_names = []
    for player in players:
        if player.name in g_players_names:
            if player.dice == 0:
                inactive_names.append(player.name)
            else:
                players_names.append(player.name)
    if inactive_names:
        print(f'Player {inactive_names[0]} left the game.')
        pause()
        return players_names
    else:
        return players_names


#  -- check which player lose a die
def check_who_lose_die(c_bidder, l_bidder, players_turns, last_bet, g_players, g_players_names, wild):
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
        print(f'There are {number_of_dices_of_searched_number} numbers of {searched_number} dices.'
              f' {l_bidder} lose a dice.')
        pause()
        remove_dice(g_players, l_bidder)
        g_players_names = players_active(g_players, g_players_names)
        choosing_player_to_start(l_bidder, g_players, g_players_names)
    else:
        print(f'There are {number_of_dices_of_searched_number} numbers of {searched_number} dices.'
              f' {c_bidder} lose a dice.')
        pause()
        remove_dice(g_players, c_bidder)
        g_players_names = players_active(g_players, g_players_names)
        choosing_player_to_start(c_bidder, g_players, g_players_names)
    return g_players_names


#  -- choose player with dice to start round --
def choosing_player_to_start(player, games_players, players_names):
    if len(players_names) > 1:
        while player != games_players[0].name:
            next_turn(games_players)
        if game_players[0].dice == 0:
            next_turn(game_players)


# -- check answer if human wants to play again with the same players--
def check_answer(human_answer):
    if human_answer.lower() == 'y':
        game_active = True
        return game_active
    elif human_answer.lower() == 'n':
        game_active = False
        return game_active
    else:
        print("Please make your choice by pressing 'y' or 'n' button on your keyboard!")
        new_human_answer = input().strip()
        check_answer(new_human_answer)


#  -- get the next bidder with dice form players --
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


#  -- human choice for game mode regular/normal or advanced/wild ones --
def choose_game_mode(human_answer):
    if human_answer.lower() == 'w':
        w_mode = True
        return w_mode
    elif human_answer.lower() == 'n':
        w_mode = False
        return w_mode
    else:
        print("Please make your choice by pressing 'w' or 'n' button on your keyboard!")
        print("By pressing 'w' you will enter advanced wild one's mode. By pressing 'n' you will play a regular game.")
        new_human_answer = input().strip()
        check_answer(new_human_answer)


# --list of 10 names of bots --
list_names_of_bots = ["Cyborg", "Terminator", "Ultron", "Vision", "J.A.R.V.I.S.", "Wall-e", "R2-D2", "C-3PO",
                      "Optimus", "Bumblebee"]

# -- initial empty list of players--
game_players = deque()

print("What is your name?")
human_player = input()
add_player(human_player)

pause(0.5)
print("Choose number of opponents.")
opponents = create_list_of_players(input().strip())

pause(0.5)
print("Choose gaming mode. Please type 'n' for regular game, or type 'w' for accessing wild one's mode")
wild_mode = choose_game_mode(input().strip())
pause()
active_game = True

while active_game:
    game_players_names = get_players_name(game_players)
    print(f"There are {len(game_players_names)} players on the table - {', '.join(game_players_names)} ")
    pause()

    print('Choosing player to start the game.')
    pause()

    starting_player_index = random.randint(0, len(game_players) - 1)
    starter = game_players[starting_player_index].name
    choosing_player_to_start(starter, game_players, game_players_names)
    print(f'{game_players[0].name} starts the game.')
    pause()

    [pl.restore_dice() for pl in game_players]
    sum_dice = 0
    players_turn = {}
    game_round = 0

    while len(game_players_names) > 1:
        sum_dice = check_sum_dice(game_players)
        game_round += 1
        old_bet = ['0', '0']
        pause()

        # -- new roll -- new round --
        players_turn = roll_dice(game_players, game_round)

        print(f'{144 * "-"}')
        print(
            f'Starting round {game_round}. '
            f'There are {len(game_players_names)} players with total {sum_dice} '
            f'dice on the table.'
        )
        pause()

        last_bidder = ''
        check_who_is_liar = False

        while not check_who_is_liar:
            while game_players[0].name not in game_players_names:
                next_turn(game_players)
            current_bidder = game_players[0].name
            liar = False
            if current_bidder == human_player:
                print(
                    f"It's your turn now! "
                    f"There are {sum_dice} dice on the table. "
                    f"You have in your hand: {players_turn[human_player]}."
                )
                pause(0.5)

                if len(last_bidder) > 0:
                    print(
                        f"What is your choice? "
                        f"Place a bet [b] or call {last_bidder} a liar [l]?"
                    )
                    human_bet = input().strip()
                    action = choose_action(human_bet)
                    pause(0.5)

                    if action == 'bet':
                        print(
                            f'What is your choice? '
                            f'Place your bet in format [count of dice] [face of die] separated by space.'
                        )
                        valid_human_bet = False
                        new_human_bet = []

                        while not valid_human_bet:
                            new_human_bet = input().strip() \
                                .split(' ')
                            valid_human_bet = valid_bet(new_human_bet, old_bet, sum_dice)
                            if not valid_human_bet:
                                print(
                                    'Please place valid bet! Place bet in format:'
                                    ' [count of dice] [face of die] separated by space.'
                                    'You should rise the last bid and type only numbers!')
                        liar, old_bet = place_bet(new_human_bet, current_bidder, game_players)
                    else:
                        liar = True
                elif old_bet == [sum_dice, 6]:
                    liar = True
                else:
                    print(
                        'Please place valid bet! Place bet in format: [count of dice] [face of die] separated by space.'
                    )
                    valid_human_bet = False
                    new_human_bet = []
                    while not valid_human_bet:
                        new_human_bet = input().strip() \
                            .split(' ')
                        valid_human_bet = valid_bet(new_human_bet, old_bet, sum_dice)
                        if not valid_human_bet:
                            print(
                                'Please place valid bet! Place bet in format:'
                                ' [count of dice] [face of die] separated by space.'
                                'You should rise the last bid and type only numbers!')
                    liar, old_bet = place_bet(new_human_bet, current_bidder, game_players)
                    pause()

            else:
                new_bet = calc_bet_according_to_temper(old_bet, current_bidder, last_bidder, sum_dice, game_players,
                                                       wild_mode)
                next_bidder = get_next_bidder(game_players)
                if new_bet:
                    if last_bidder == '':
                        while int(new_bet[0]) > (sum_dice - next_bidder.dice):
                            new_bet_to_be_checked_again = bluff_bet(
                                old_bet, sum_dice, current_bidder, last_bidder, game_players, wild_mode, 0)
                            new_bet = new_bet_to_be_checked_again
                    else:
                        if int(new_bet[0]) > (sum_dice - next_bidder.dice):
                            new_bet = []

                if len(new_bet) == 0:
                    print_if_liar(current_bidder, last_bidder, players_turn)
                    game_players_names = check_who_lose_die(current_bidder, last_bidder, players_turn, old_bet,
                                                            game_players, game_players_names, wild_mode)

                    check_if_players_are_bluffing(game_players, wild_mode)
                    check_who_is_liar = True
                    break
                elif old_bet == [sum_dice, 6]:
                    liar = True
                elif new_bet[0] > (sum_dice - next_bidder.dice) and last_bidder != '':
                    liar = True
                else:
                    liar, old_bet = place_bet(new_bet, current_bidder, game_players)

            if liar:
                pause()
                print_if_liar(current_bidder, last_bidder, players_turn)
                game_players_names = check_who_lose_die(current_bidder, last_bidder, players_turn, old_bet,
                                                        game_players, game_players_names, wild_mode)
                check_if_players_are_bluffing(game_players, wild_mode)
                check_who_is_liar = True
                break
            last_bidder = current_bidder
            next_turn(game_players)
            sum_dice = check_sum_dice(game_players)
            check_who_is_liar = False

    print(
        f'The winner is {game_players_names[0]}. '
        f'Congratulations!'
    )
    pause()

    print(
        'Do you like to start again? '
        '[y/n]'
    )
    answer = input().strip()
    check_answer(answer)
    pause()
