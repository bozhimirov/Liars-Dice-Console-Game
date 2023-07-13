from collections import deque

from helper_functions import choose_language
from pause import pause
from player import Player


# -- print asks for choice --
def ask_for_choice(english_language: bool) -> None:
    choose_language(english_language, 'What is your choice?', 'Какъв е твоят избор?')


# -- function to print text on console asking for game language--
def text_choose_language() -> None:
    print("Choose language/Избери език")
    print("Please type 'e' for English or/или напишете 'b' за Български")


# -- function to print text on console asking for player's name--
def text_choose_name(english_language: bool) -> None:
    choose_language(english_language, "What is your name?", "Какво е вашето име?")


# -- function to print text on console asking for number of opponents--
def text_choose_opponents(english_language: bool) -> None:
    choose_language(english_language, "Choose number of opponents.", "Изберете броя на противниците си.")


# -- function to print text on console asking for game mode--
def text_choose_mode(english_language: bool) -> None:
    choose_language(english_language, "Choose gaming mode. Please type 'n' for regular game, or type 'w' for accessing "
                                      "wild one's mode.", "Изберете ниво на трудност. Моля напишете 'n' за обикновена "
                                                          "игра или напишете 'w' за да влезете в режим 'луди единици'.")


# -- function to print text on console telling number of active players--
def text_tell_len_players(english_language: bool, game_players_names: list) -> None:
    choose_language(english_language,
                    f"There are {len(game_players_names)} players on the table - {', '.join(game_players_names)} ",
                    f"Има {len(game_players_names)} играчи на масата - {', '.join(game_players_names)} ")
    pause()


# -- function to print text on console telling choosing player to start--
def text_choosing_player(english_language: bool) -> None:
    choose_language(english_language, 'Choosing player to start the game.', 'Избира се играч, който да започне играта.')
    pause()


# -- function to print text on console telling who starts the game--
def text_who_starts_the_game(english_language: bool, game_players: deque) -> None:
    choose_language(english_language, f'{game_players[0].name} starts the game.',
                    f'{game_players[0].name} започва играта.')
    pause()


# -- prints line with num len --
def line(num: int) -> None:
    print(f'{num * "-"}')


# -- print new round text and players with dice--
def text_new_round_number(english_language: bool, game_round: int, game_players_names: list, sum_dice: int) -> None:
    choose_language(english_language, f'Starting round {game_round}.', f'Започва рунд {game_round}.')
    choose_language(english_language,
                    f'There are {len(game_players_names)} players with total {sum_dice} dice on the table.',
                    f'Има {len(game_players_names)} играчи с общо {sum_dice} зарове на масата.')
    pause()


# -- print it is your turn and tell info about total dice and own dice--
def text_your_turn_and_info(english_language: bool, sum_dice: int, players_turn: dict, human_player: str) -> None:
    choose_language(english_language, "It's your turn now!", "Твой ред е!")
    pause(1)
    choose_language(english_language, f"There are {sum_dice} dice on the table.",
                    f"Има {sum_dice} зарчета на масата.")
    pause(1)
    choose_language(english_language, f"You have in your hand: {players_turn[human_player]}.",
                    f"В ръката си имаш: {players_turn[human_player]}.")
    pause()


# -- print text if there is a last winner with options for bet or call liar--
def text_if_there_is_last_bidder(english_language: bool, last_bidder: str) -> None:
    ask_for_choice(english_language)
    choose_language(english_language, f"Place a bet [b] or call {last_bidder} a liar [l]?",
                    f"Направи залог [b] или наречи {last_bidder} лъжец [l]?")


# -- print text asking valid bet --
def text_place_bet(english_language: bool) -> None:
    ask_for_choice(english_language)
    choose_language(english_language,
                    'Place your bet in format [count of dice] [face of die] separated by space.',
                    'Направи залог във формат [брой зарове] [стойност на зара] разделени с интервал.')


# -- print announcement of winner and congrats --
def text_tell_winner(english_language: bool, game_players_names: list) -> None:
    choose_language(english_language, f'The winner is {game_players_names[0]}.',
                    f'Победителят е {game_players_names[0]}.')
    choose_language(english_language, 'Congratulations!', 'Поздравления!')
    pause()


# -- print aks for a new game --
def text_new_game_option(english_language: bool) -> None:
    choose_language(english_language, 'Do you like to start again?', 'Искаш ли да играеш отново?')
    print(
        '[y/n]'
    )


# -- print the bet of the player --
def text_player_bet(language: bool, player: Player, current_bet: list) -> None:
    choose_language(language,
                    f'{player} bet for at least {current_bet[0]} dice with face number {current_bet[1]}.',
                    f'{player} залага за най-малко {current_bet[0]} зарове със стойност {current_bet[1]}.')
    pause()


# --  print asks for valid action again --
def text_valid_action_again(language: bool) -> None:
    choose_language(language, "Please make a valid choice! Type 'b' or 'l'. ", "Моля направете валиден избор! "
                                                                               "Напишете 'b' или 'l'. ")


# -- print asks for length more than 2 symbols --
def text_name_len_more_than_two(language: bool) -> None:
    choose_language(language, "Please write a name longer than 2 symbols!",
                    "Моля напишете име с дължина повече от 2 символа!")


# -- print ask for valid choice --
def text_make_valid_choice(language: bool) -> None:
    choose_language(language, "Please make your choice by pressing 'y' or 'n' button on your keyboard!",
                    "Моля направете избор като натиснете 'y' или 'n' бутона на клавиатурата си!")


# -- print ask for valid mode --
def text_choose_valid_mode(language: bool) -> None:
    choose_language(language, "Please make your choice by pressing 'w' or 'n' button on your keyboard!",
                    "Моля направете своя избор като натиснете 'w' или 'n' бутона на клавиатурата си!")
    choose_language(language, "By pressing 'w' you will enter advanced wild one's mode. By pressing 'n' you will "
                              "play a regular game.", "Натискайки 'w' ще задействате режима на лудите единици. "
                                                      "Натискайки 'n' ще играете обикновена игра.")


# -- print ask for valid bet again --
def text_valid_bet_again(language: bool) -> None:
    choose_language(language, 'Please place valid bet! Place bet in format: '
                              '[count of dice] [face of die] separated by space.'
                              'You should rise the last bid and type only numbers!',
                    'Моля направете валиден залог! Напишете залог във формат: '
                    '[брой зарове] [стойност на зара] разделени с интервал.'
                    'Трябва да вдигнете последният залог и да пишете само с цифри!')


# -- print ask for valid language choice --
def text_valid_language() -> None:
    print("Please make your choice by pressing 'e' or 'b' button on your keyboard!")
    print("Моля натиснете 'e' или 'b' бутона на клавиатурата!")
    print("By pressing 'е' you will play the game in English. By pressing 'b' you will play the game in Bulgarian.")
    print("Натискайки 'e' ще играете играта на английски език. Натискайки 'b' ще играете играта на български език.")


# -- print ask for new name --
def text_choose_name_again(language: bool) -> None:
    choose_language(language, "Name taken, please choose another username.",
                    "Името е заето, моля изберете друго име.")


# -- print ask for new number of opponents --
def text_incorrect_input_opponents(language: bool) -> None:
    choose_language(language,
                    "Incorrect input. Please type just one number for opponents between 1 and 10.",
                    "Грешна стойност. Моля напишете само едно число за брой противници в интервала от 1 до 10.")


# -- print who left the game --
def text_left_game(language: bool, inactive_names: list) -> None:
    choose_language(language, f'Player {inactive_names[0]} left the game.',
                    f'Играч {inactive_names[0]} напусна играта.')
    pause()


# -- print result and who lost a die --
def text_result_and_who_lose_die(language: bool, number_of_dices_of_searched_number: int, searched_number: int,
                                 l_bidder: Player) -> None:
    choose_language(language,
                    f'There are {number_of_dices_of_searched_number} numbers of {searched_number} dices. {l_bidder} '
                    f'lose a dice.',
                    f'Има {number_of_dices_of_searched_number} броя зарове със стойност {searched_number}. {l_bidder}'
                    f' губи зарче.')
    pause()


# -- print someone call other liar --
def text_someone_call_other_liar(language: bool, current_player: str, last_player: str) -> None:
    choose_language(language, f'{current_player} called {last_player} a liar. Everyone showing their dice.',
                    f'{current_player} нарече {last_player} лъжец. Всички играчи показват заровете си.')
    pause()


# -- get verb according to language --
def get_verb(language: bool) -> str:
    if language:
        return ' has '
    else:
        return ' има '
