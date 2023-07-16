from helper_functions import choose_language
from pause import pause
from player import Player
from print import Print


# -- function to print text on console telling number of active players--
def text_tell_len_players(self, game_players_names) -> None:
    choose_language(self.english_language,
                    f"There are {len(game_players_names)} players on the table - "
                    f"{', '.join(game_players_names)} ",
                    f"Има {len(game_players_names)} играчи на масата - "
                    f"{', '.join(game_players_names)} ")
    pause()


# -- function to print text on console telling who starts the game--
def text_who_starts_the_game(self, game_players) -> None:
    choose_language(self.english_language, f'{game_players[0].name} starts the game.',
                    f'{game_players[0].name} започва играта.')
    pause()


# -- print new round text and players with dice--
def text_new_round_number(self, game_round, game_players_names: list, sum_dice: int) -> None:
    choose_language(self.english_language, f'Starting round {game_round}.', f'Започва рунд {game_round}.')
    choose_language(self.english_language,
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
    Print.ask_for_choice()
    choose_language(english_language, f"Place a bet [b] or call {last_bidder} a liar [l]?",
                    f"Направи залог [b] или наречи {last_bidder} лъжец [l]?")


# -- print announcement of winner and congrats --
def text_tell_winner(english_language: bool, game_players_names: list) -> None:
    choose_language(english_language, f'The winner is {game_players_names[0]}.',
                    f'Победителят е {game_players_names[0]}.')
    choose_language(english_language, 'Congratulations!', 'Поздравления!')
    pause()


# -- print the bet of the player --
def text_player_bet(language: bool, player: Player, current_bet: list) -> None:
    choose_language(language,
                    f'{player} bet for at least {current_bet[0]} dice with face number {current_bet[1]}.',
                    f'{player} залага за най-малко {current_bet[0]} зарове със стойност {current_bet[1]}.')
    pause()


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
