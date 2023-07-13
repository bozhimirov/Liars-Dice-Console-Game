import random
from collections import deque

from player import Player
from player_helpers import get_player_by_name, add_turns_to_player
from probability_calculation import calculate_probability
from stats_memory_players import load_memory
from text_instructions import text_player_bet
from validators import valid_bet


# --calculate test new  bet --
def calculate_new_bet(last_bet: list, player: Player, last_player: Player, sum_of_dice: int, players: deque, wild: bool,
                      opponents_chance: float) -> list:
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
def if_not_blank_bet(player: Player, last_bet: list, opponents_chance: float, sum_of_dice: int, players: deque,
                     wild: bool, last_player: Player) -> list:
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


# -- place bet on table --
def place_bet(current_bet: list, player: Player, players: deque, language: bool) -> list:
    load_memory(player, current_bet, players)
    add_turns_to_player(player, players)
    text_player_bet(language, player, current_bet)
    previous_bet = current_bet
    liar_statement = False
    return [liar_statement, previous_bet]


#  -- according to temper and times player places bet in the round, choose if the bet is bluff or not --
def calc_bet_according_to_temper(last_bet: list, current_player: Player, last_player: Player, sum_of_dice: int,
                                 players: deque, wild: bool) -> list:
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


#  -- calculate bluff bet --
def dice_modifier(prev_dice: int, wild: bool) -> list:
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

    return [prev_dice, new_dice]


def bluff_bet(prev_bet: list, sum_of_dice: int, current_player: Player, last_player: Player, players: deque, wild: bool,
              opponents_chance: float) -> list:
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
                        dice_modifier(prev_dice, wild)
                        new_bet_to_be_checked = [new_count, new_dice]
                        valid_condition = valid_bet(new_bet_to_be_checked, prev_bet, sum_of_dice)
                        if valid_condition:
                            break
                new_bet_to_be_checked = [new_count, new_dice]
                valid_condition = valid_bet(new_bet_to_be_checked, prev_bet, sum_of_dice)
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
                dice_modifier(prev_dice, wild)
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
                valid_condition = valid_bet(new_bet_to_be_checked, prev_bet, sum_of_dice)
                if valid_condition:
                    break
        new_bet_to_be_checked = [new_count, new_dice]
        valid_condition = valid_bet(new_bet_to_be_checked, prev_bet, sum_of_dice)
        if valid_condition:
            return new_bet_to_be_checked
    return []
