import math

from player import Player


#  -- calculate probability using binomial distribution--
def calculate_probability(bet: list, sum_of_dice: int, current_player: Player, wild: bool,
                          keyword: str = 'stat') -> float:
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
