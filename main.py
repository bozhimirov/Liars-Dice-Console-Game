import random
from collections import deque

from betting_helpers import calc_bet_according_to_temper, bluff_bet, place_bet
from helper_functions import check_sum_dice, roll_dice
from pause import pause
from player_helpers import add_player, create_list_of_players, get_players_name, choosing_player_to_start, next_turn, \
    get_next_bidder, print_if_liar, check_who_lose_die, check_if_players_are_bluffing
from text_instructions import text_choose_language, text_choose_name, text_choose_opponents, text_choose_mode, \
    text_tell_len_players, text_choosing_player, text_who_starts_the_game, line, text_new_round_number, \
    text_your_turn_and_info, text_if_there_is_last_bidder, text_place_bet, text_tell_winner, \
    text_new_game_option
from validators import validate_language, validate_name, validate_game_mode, validate_input_action, \
    validate_if_bet_is_valid, validate_input_answer

# --list of 10 names of bots --
list_names_of_bots = ["Cyborg", "Terminator", "Ultron", "Vision", "J.A.R.V.I.S.", "Wall-e", "R2-D2", "C-3PO",
                      "Optimus", "Bumblebee"]

# -- initial empty list of players--
game_players = deque()

text_choose_language()
english_language = validate_language(input().strip())

text_choose_name(english_language)
human_player = validate_name(input().strip(), english_language)
add_player(human_player, list_names_of_bots, game_players, english_language)

pause(0.5)

text_choose_opponents(english_language)
opponents = create_list_of_players(input().strip(), list_names_of_bots, game_players, english_language)

pause(0.5)

text_choose_mode(english_language)
wild_mode = validate_game_mode(input().strip(), english_language)

pause(0.5)

active_game = True

# -- new game --
while active_game:
    game_players_names = get_players_name(game_players)
    text_tell_len_players(english_language, game_players_names)
    text_choosing_player(english_language)
    starting_player_index = random.randint(0, len(game_players) - 1)
    starter = game_players[starting_player_index].name
    choosing_player_to_start(starter, game_players, game_players_names)
    text_who_starts_the_game(english_language, game_players)
    [pl.restore_dice() for pl in game_players]
    sum_dice = 0
    players_turn = {}
    game_round = 0

# -- new round--
    while len(game_players_names) > 1:
        last_bidder = ''
        check_who_is_liar = False

        sum_dice = check_sum_dice(game_players)
        game_round += 1
        old_bet = ['0', '0']

        # -- new roll --
        players_turn = roll_dice(game_players, game_round)
        line(60)
        text_new_round_number(english_language, game_round, game_players_names, sum_dice)

        while not check_who_is_liar:
            while game_players[0].name not in game_players_names:
                next_turn(game_players)
            current_bidder = game_players[0].name
            liar = False
            if current_bidder == human_player:
                text_your_turn_and_info(english_language, sum_dice, players_turn, human_player)

                if len(last_bidder) > 0:
                    text_if_there_is_last_bidder(english_language, last_bidder)
                    human_bet = input().strip()
                    action = validate_input_action(human_bet, english_language)
                    pause(0.5)

                    if action == 'bet':
                        text_place_bet(english_language)
                        new_human_bet = validate_if_bet_is_valid(old_bet, sum_dice, english_language)
                        liar, old_bet = place_bet(new_human_bet, current_bidder, game_players, english_language)

                    else:
                        liar = True
                elif old_bet == [sum_dice, 6]:
                    liar = True
                else:
                    text_place_bet(english_language)
                    new_human_bet = validate_if_bet_is_valid(old_bet, sum_dice, english_language)
                    liar, old_bet = place_bet(new_human_bet, current_bidder, game_players, english_language)

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
                    print_if_liar(current_bidder, last_bidder, players_turn, english_language)
                    game_players_names = check_who_lose_die(current_bidder, last_bidder, players_turn, old_bet,
                                                            game_players, game_players_names, wild_mode,
                                                            english_language)

                    check_if_players_are_bluffing(game_players, wild_mode)
                    check_who_is_liar = True
                    break
                elif old_bet == [sum_dice, 6]:
                    liar = True
                elif new_bet[0] > (sum_dice - next_bidder.dice) and last_bidder != '':
                    liar = True
                else:
                    liar, old_bet = place_bet(new_bet, current_bidder, game_players, english_language)

            if liar:
                pause()
                print_if_liar(current_bidder, last_bidder, players_turn, english_language)
                game_players_names = check_who_lose_die(current_bidder, last_bidder, players_turn, old_bet,
                                                        game_players, game_players_names, wild_mode, english_language)
                check_if_players_are_bluffing(game_players, wild_mode)
                check_who_is_liar = True
                break
            last_bidder = current_bidder
            next_turn(game_players)
            pause()
            sum_dice = check_sum_dice(game_players)
            check_who_is_liar = False

    text_tell_winner(english_language, game_players_names)
    text_new_game_option(english_language)

    answer = input().strip()
    active_game = validate_input_answer(answer, english_language)
    pause()