from print import Print


# -- choose human action - bet or liar --
def validate_input_action(string: str, language: bool) -> str:
    if string.lower() == 'b':
        return 'bet'
    elif string.lower() == 'l':
        return 'liar'
    else:
        Print.text_valid_action_again()
        new_human_string = input().strip()
        human_action = validate_input_action(new_human_string, language)
        return human_action


# -- validate name of human player / cannot be blank / --
def validate_name(name: str, language: bool) -> str:
    if len(name) < 2:
        Print.text_name_len_more_than_two()
        new_human_name = input().strip()
        new_name = validate_name(new_human_name, language)
        return new_name
    return name


# -- check answer if human wants to play again with the same players--
def validate_input_answer(human_answer: str, language: bool) -> bool:
    if human_answer.lower() == 'y':
        game_active = True
        return game_active
    elif human_answer.lower() == 'n':
        game_active = False
        return game_active
    else:
        Print.text_make_valid_choice()
        new_human_answer = input().strip()
        new_game_active = validate_input_answer(new_human_answer, language)
        return new_game_active


#  -- human choice for game mode regular/normal or advanced/wild ones --
def validate_game_mode(human_answer: str, language: bool) -> bool:
    if human_answer.lower() == 'w':
        w_mode = True
        return w_mode
    elif human_answer.lower() == 'n':
        w_mode = False
        return w_mode
    else:
        Print.text_choose_valid_mode()
        new_human_answer = input().strip()
        new_w_mode = validate_input_answer(new_human_answer, language)
        return new_w_mode


def validate_if_bet_is_valid(old_bet: list, sum_dice: int) -> list:
    valid_human_bet = False
    new_human_bet = []
    while not valid_human_bet:
        new_human_bet = input().strip() \
            .split(' ')
        valid_human_bet = valid_bet(new_human_bet, old_bet, sum_dice)
        if not valid_human_bet:
            Print.text_valid_bet_again()
    return new_human_bet


# -- validate bets --
def valid_bet(current_bet: list, previous_bet: list, sum_of_dice: int) -> bool:
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
                if int(current_bet[1]) > 6:
                    return False
                return True
            else:
                return False


#  -- human choice for language preferences --
def validate_language(human_answer: str) -> bool:
    if human_answer.lower() == 'e':
        return True
    elif human_answer.lower() == 'b':
        return False
    else:
        Print.text_valid_language()
        new_human_answer = input().strip()
        language = validate_language(new_human_answer)
        return language
