import random
from collections import deque

from betting_helpers import check_if_bet_is_valid, calc_bet_according_to_temper, bluff_bet, place_bet
from helper_functions import choose_game_mode, choose_action, check_answer, check_sum_dice, roll_dice
from language_helpers import check_language, choose_language
from pause import pause
from player_helpers import add_player, create_list_of_players, get_players_name, choosing_player_to_start, next_turn, \
    get_next_bidder, print_if_liar, check_who_lose_die, check_if_players_are_bluffing

# --list of 10 names of bots --
list_names_of_bots = ["Cyborg", "Terminator", "Ultron", "Vision", "J.A.R.V.I.S.", "Wall-e", "R2-D2", "C-3PO",
                      "Optimus", "Bumblebee"]

# -- initial empty list of players--
game_players = deque()
print("Choose language/Избери език")
print("Please type 'e' for English or/или напишете 'b' за Български")
english_language = choose_language(input().strip())
check_language(english_language, "What is your name?", "Какво е вашето име?")
human_player = input()
add_player(human_player, list_names_of_bots, game_players, english_language)

pause(0.5)
check_language(english_language, "Choose number of opponents.", "Изберете броя на противниците си.")
opponents = create_list_of_players(input().strip(), list_names_of_bots, game_players, english_language)

pause(0.5)
check_language(english_language, "Choose gaming mode. Please type 'n' for regular game, or type 'w' for accessing "
                                 "wild one's mode.", "Изберете ниво на трудност. Моля напишете 'n' за обикновена игра "
                                                     "или напишете 'w' за да влезете в режим 'луди единици'.")

wild_mode = choose_game_mode(input().strip(), english_language)
pause(0.5)
active_game = True

while active_game:
    game_players_names = get_players_name(game_players)
    check_language(english_language,
                   f"There are {len(game_players_names)} players on the table - {', '.join(game_players_names)} ",
                   f"Има {len(game_players_names)} играчи на масата - {', '.join(game_players_names)} ")
    pause()

    check_language(english_language, 'Choosing player to start the game.', 'Избира се играч, който да започне играта.')
    pause()

    starting_player_index = random.randint(0, len(game_players) - 1)
    starter = game_players[starting_player_index].name
    choosing_player_to_start(starter, game_players, game_players_names)
    check_language(english_language, f'{game_players[0].name} starts the game.',
                   f'{game_players[0].name} започва играта.')
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

        print(f'{60 * "-"}')
        check_language(english_language, f'Starting round {game_round}.', f'Започва рунд {game_round}.')
        check_language(english_language,
                       f'There are {len(game_players_names)} players with total {sum_dice} dice on the table.',
                       f'Има {len(game_players_names)} играчи с общо {sum_dice} зарове на масата.')
        pause()

        last_bidder = ''
        check_who_is_liar = False

        while not check_who_is_liar:
            while game_players[0].name not in game_players_names:
                next_turn(game_players)
            current_bidder = game_players[0].name
            liar = False
            if current_bidder == human_player:
                check_language(english_language, "It's your turn now!", "Твой ред е!")
                pause(0.5)
                check_language(english_language, f"There are {sum_dice} dice on the table.",
                               f"Има {sum_dice} зарчета на масата.")
                pause(0.5)
                check_language(english_language, f"You have in your hand: {players_turn[human_player]}.",
                               f"В ръката си имаш: {players_turn[human_player]}.")
                pause()

                if len(last_bidder) > 0:
                    check_language(english_language, "What is your choice?", "Какъв е твоят избор?")
                    check_language(english_language, f"Place a bet [b] or call {last_bidder} a liar [l]?",
                                   f"Направи залог [b] или наречи {last_bidder} лъжец [l]?")
                    human_bet = input().strip()
                    action = choose_action(human_bet, english_language)
                    pause()

                    if action == 'bet':
                        check_language(english_language, 'What is your choice?', 'Какъв е твоят избор?')
                        check_language(english_language,
                                       'Place your bet in format [count of dice] [face of die] separated by space.',
                                       'Направи залог във формат [брой зарове] [стойност на зара] разделени с интервал.')
                        check_if_bet_is_valid(old_bet, sum_dice, game_players, current_bidder, english_language)

                    else:
                        liar = True
                elif old_bet == [sum_dice, 6]:
                    liar = True
                else:
                    check_language(english_language,
                                   'Please place valid bet! Place your bet in format [count of dice] [face of die] '
                                   'separated by space.',
                                   'Направи валиден залог! Направи залог във формат [брой зарове] [стойност на зара] '
                                   'разделени с интервал.')
                    check_if_bet_is_valid(old_bet, sum_dice, game_players, current_bidder, english_language)
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
                                                            game_players, game_players_names, wild_mode, english_language)

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
            sum_dice = check_sum_dice(game_players)
            check_who_is_liar = False

    check_language(english_language, f'The winner is {game_players_names[0]}.',
                   f'Победителят е {game_players_names[0]}.')
    check_language(english_language, 'Congratulations!', 'Поздравления!')
    pause()

    check_language(english_language, 'Do you like to start again?', 'Искаш ли да играеш отново?')
    print(
        '[y/n]'
    )
    answer = input().strip()
    check_answer(answer, english_language)
    pause()
