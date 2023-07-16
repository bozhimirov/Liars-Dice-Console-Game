from helper_functions import choose_language
from pause import pause


class Print:
    def __init__(self, english_language: bool) -> None:
        self.english_language = english_language
        self.num = 60

    # -- function to print text on console asking for game language--
    @classmethod
    def text_choose_language(cls) -> None:
        print("Choose language/Избери език")
        print("Please type 'e' for English or/или напишете 'b' за Български")

    # -- print ask for valid language choice --
    @classmethod
    def text_valid_language(cls) -> None:
        print("Please make your choice by pressing 'e' or 'b' button on your keyboard!")
        print("Моля натиснете 'e' или 'b' бутона на клавиатурата!")
        print("By pressing 'е' you will play the game in English. By pressing 'b' you will play the game in Bulgarian.")
        print("Натискайки 'e' ще играете играта на английски език. Натискайки 'b' ще играете играта на български език.")

    # -- function to print text on console asking for player's name--
    def text_choose_name(self) -> None:
        choose_language(self.english_language, "What is your name?", "Какво е вашето име?")

    # -- print asks for choice --
    def ask_for_choice(self) -> None:
        choose_language(self.english_language, 'What is your choice?', 'Какъв е твоят избор?')

    # -- function to print text on console asking for number of opponents--
    def text_choose_opponents(self) -> None:
        choose_language(self.english_language, "Choose number of opponents.", "Изберете броя на противниците си.")

    # -- function to print text on console asking for game mode--
    def text_choose_mode(self) -> None:
        choose_language(self.english_language,
                        "Choose gaming mode. Please type 'n' for regular game, or type 'w' for accessing "
                        "wild one's mode.", "Изберете ниво на трудност. Моля напишете 'n' за обикновена "
                                            "игра или напишете 'w' за да влезете в режим 'луди единици'.")

    # -- function to print text on console telling choosing player to start--
    def text_choosing_player(self) -> None:
        choose_language(self.english_language, 'Choosing player to start the game.',
                        'Избира се играч, който да започне играта.')
        pause()

    # -- prints line with num len --
    def line(self) -> None:
        print(f'{self.num * "-"}')

    # -- print text asking valid bet --
    def text_place_bet(self) -> None:
        self.ask_for_choice()
        choose_language(self.english_language,
                        'Place your bet in format [count of dice] [face of die] separated by space.',
                        'Направи залог във формат [брой зарове] [стойност на зара] разделени с интервал.')

    # -- print aks for a new game --
    def text_new_game_option(self) -> None:
        choose_language(self.english_language, 'Do you like to start again?', 'Искаш ли да играеш отново?')
        print(
            '[y/n]'
        )

    # --  print asks for valid action again --
    def text_valid_action_again(self) -> None:
        choose_language(self.english_language, "Please make a valid choice! Type 'b' or 'l'. ",
                        "Моля направете валиден избор! Напишете 'b' или 'l'. ")

    # -- print asks for length more than 2 symbols --
    def text_name_len_more_than_two(self) -> None:
        choose_language(self.english_language, "Please write a name longer than 2 symbols!",
                        "Моля напишете име с дължина повече от 2 символа!")

    # -- print ask for valid choice --
    def text_make_valid_choice(self) -> None:
        choose_language(self.english_language, "Please make your choice by pressing 'y' or 'n' button on your keyboard!",
                        "Моля направете избор като натиснете 'y' или 'n' бутона на клавиатурата си!")

    # -- print ask for valid mode --
    def text_choose_valid_mode(self) -> None:
        choose_language(self.english_language, "Please make your choice by pressing 'w' or 'n' button on your keyboard!",
                        "Моля направете своя избор като натиснете 'w' или 'n' бутона на клавиатурата си!")
        choose_language(self.english_language, "By pressing 'w' you will enter advanced wild one's mode. By pressing 'n' you will "
                                  "play a regular game.", "Натискайки 'w' ще задействате режима на лудите единици. "
                                                          "Натискайки 'n' ще играете обикновена игра.")

    # -- print ask for valid bet again --
    def text_valid_bet_again(self) -> None:
        choose_language(self.english_language, 'Please place valid bet! Place bet in format: '
                                  '[count of dice] [face of die] separated by space.'
                                  'You should rise the last bid and type only numbers!',
                        'Моля направете валиден залог! Напишете залог във формат: '
                        '[брой зарове] [стойност на зара] разделени с интервал.'
                        'Трябва да вдигнете последният залог и да пишете само с цифри!')

    # -- print ask for new name --
    def text_choose_name_again(self) -> None:
        choose_language(self.english_language, "Name taken, please choose another username.",
                        "Името е заето, моля изберете друго име.")

    # -- print ask for new number of opponents --
    def text_incorrect_input_opponents(self) -> None:
        choose_language(self.english_language,
                        "Incorrect input. Please type just one number for opponents between 1 and 10.",
                        "Грешна стойност. Моля напишете само едно число за брой противници в интервала от 1 до 10.")

    # -- get verb according to language --
    def get_verb(self) -> str:
        if self.english_language:
            return ' has '
        else:
            return ' има '
