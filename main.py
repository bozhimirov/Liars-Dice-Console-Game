import random
from collections import deque

from betting_helpers import calc_bet_according_to_temper, bluff_bet, place_bet
from helper_functions import check_sum_dice, roll_dice
from pause import pause
from player_helpers import add_player, create_list_of_players, get_players_name, choosing_player_to_start, next_turn, \
    get_next_bidder, print_if_liar, check_who_lose_die, check_if_players_are_bluffing
from text_instructions import text_tell_len_players, text_who_starts_the_game, text_new_round_number, \
    text_your_turn_and_info, text_if_there_is_last_bidder, text_tell_winner
from validators import validate_language, validate_name, validate_game_mode, validate_input_action, \
    validate_if_bet_is_valid, validate_input_answer
from print import Print


class Game:
    def __init__(self):
        # --list of 10 names of bots --
        self.list_names_of_bots = ["Cyborg", "Terminator", "Ultron", "Vision", "J.A.R.V.I.S.", "Wall-e", "R2-D2",
                                   "C-3PO", "Optimus", "Bumblebee"]
        # -- initial empty list of players--
        self.game_players = deque()
        self.english_language = True
        self.number_of_opponents = 0
        self.wild_mode = False
        self.active_game = True
        self.players_names = []
        self.last_bidder = ''
        self.check_who_is_liar = False
        self.old_bet = ['0', '0']
        self.sum_dice = 0
        self.players_turn = {}
        self.game_round = 0
        self.liar = False
        self.human_player_name = ''

    @staticmethod
    def language():
        Print.text_choose_language()
        english_language = validate_language(input().strip())
        return english_language

    def create_human_player(self, player_input_name: str) -> None:
        Print.text_choose_name(self)
        self.human_player_name = validate_name(player_input_name.strip(), self.english_language)
        add_player(self.human_player_name, self.list_names_of_bots, self.game_players, self.english_language)
        pause(0.5)

    def create_opponents(self, player_input_bots):
        Print.text_choose_opponents(self)
        self.number_of_opponents = create_list_of_players(player_input_bots.strip(), self.list_names_of_bots,
                                                          self.game_players, self.english_language)
        pause(0.5)

    def choose_mode(self, player_input_mode):
        Print.text_choose_mode(self)
        self.wild_mode = validate_game_mode(player_input_mode.strip(), self.english_language)
        pause(0.5)

    def choose_end(self, player_input_end):
        # answer = input().strip()
        self.active_game = validate_input_answer(player_input_end.strip(), self.english_language)
        pause()

    def new_game(self):

        self.sum_dice = 0
        self.players_turn = {}
        self.game_round = 0

        while self.active_game:
            self.players_names = get_players_name(self.game_players)
            text_tell_len_players(self.english_language, self.players_names)
            Print.text_choosing_player(self)
            index_of_player_index = random.randint(0, len(self.game_players) - 1)
            starter_player = self.game_players[index_of_player_index].name
            choosing_player_to_start(starter_player, self.game_players, self.players_names)
            text_who_starts_the_game(self.english_language, self.game_players)
            [pl.restore_dice() for pl in self.game_players]

            self.new_round()

            text_tell_winner(self.english_language, self.players_names)
            Print.text_new_game_option(self)

            self.choose_end(input())

    def new_round(self):
        while len(self.players_names) > 1:
            self.sum_dice = check_sum_dice(self.game_players)
            self.game_round += 1

            self.new_roll()
            self.while_not_liar()

    def new_roll(self):
        self.players_turn = roll_dice(self.game_players, self.game_round)
        Print.line(self)
        text_new_round_number(self.english_language, self.game_round, self.players_names, self.sum_dice)

    def human_bet(self, player_input_bet):
        action = validate_input_action(player_input_bet.strip(), self.english_language)
        pause(0.5)
        return action

    def while_not_liar(self):
        while not self.check_who_is_liar:
            while self.game_players[0].name not in self.players_names:
                next_turn(self.game_players)
            current_bidder = self.game_players[0].name
            if current_bidder == self.human_player_name:
                text_your_turn_and_info(self.english_language, self.sum_dice, self.players_turn, self.human_player_name)

                if len(self.last_bidder) > 0:
                    text_if_there_is_last_bidder(self.english_language, self.last_bidder)

                    action = self.human_bet(input())

                    if action == 'bet':
                        Print.text_place_bet(self)
                        new_human_bet = validate_if_bet_is_valid(self.old_bet, self.sum_dice)
                        liar, old_bet = place_bet(new_human_bet, current_bidder, self.game_players,
                                                  self.english_language)

                    else:
                        liar = True
                elif self.old_bet == [self.sum_dice, 6]:
                    liar = True
                else:
                    Print.text_place_bet(self)
                    new_human_bet = validate_if_bet_is_valid(self.old_bet, self.sum_dices)
                    liar, old_bet = place_bet(new_human_bet, current_bidder, self.game_players, self.english_language)

                pause()

            else:
                new_bet = calc_bet_according_to_temper(self.old_bet, current_bidder, self.last_bidder, self.sum_dice,
                                                       self.game_players, self.wild_mode)
                next_bidder = get_next_bidder(self.game_players)
                if new_bet:
                    if self.last_bidder == '':
                        while int(new_bet[0]) > (self.sum_dice - next_bidder.dice):
                            new_bet_to_be_checked_again = bluff_bet(
                                self.old_bet, self.sum_dice, current_bidder, self.last_bidder, self.game_players,
                                self.wild_mode, 0)
                            new_bet = new_bet_to_be_checked_again
                    else:
                        if int(new_bet[0]) > (self.sum_dice - next_bidder.dice):
                            new_bet = []

                if len(new_bet) == 0:
                    print_if_liar(current_bidder, self.last_bidder, self.players_turn, self.english_language)
                    self.players_names = check_who_lose_die(current_bidder, self.last_bidder, self.players_turn,
                                                            self.old_bet, self.game_players, self.players_names,
                                                            self.wild_mode, self.english_language)

                    check_if_players_are_bluffing(self.game_players, self.wild_mode)
                    self.check_who_is_liar = True
                    break
                elif self.old_bet == [self.sum_dice, 6]:
                    liar = True
                elif new_bet[0] > (self.sum_dice - next_bidder.dice) and self.last_bidder != '':
                    liar = True
                else:
                    liar, old_bet = place_bet(new_bet, current_bidder, self.game_players, self.english_language)

            if liar:
                pause()
                print_if_liar(current_bidder, self.last_bidder, self.players_turn, self.english_language)
                self.players_names = check_who_lose_die(current_bidder, self.last_bidder, self.players_turn,
                                                        self.old_bet, self.game_players, self.players_names,
                                                        self.wild_mode, self.english_language)
                check_if_players_are_bluffing(self.game_players, self.wild_mode)
                self.check_who_is_liar = True
                break
            self.last_bidder = current_bidder
            next_turn(self.game_players)
            pause()
            self.sum_dice = check_sum_dice(self.game_players)
            self.check_who_is_liar = False

    def run(self):
        self.language()
        self.create_human_player(input())
        self.create_opponents(input())
        self.choose_mode(input())
        self.new_game()


if __name__ == "__main__":
    game = Game()
    game.run()
