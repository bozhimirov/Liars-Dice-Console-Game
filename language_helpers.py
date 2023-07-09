

#  -- human choice for language preferences --
def choose_language(human_answer):
    if human_answer.lower() == 'e':
        return True
    elif human_answer.lower() == 'b':
        return False
    else:
        print("Please make your choice by pressing 'e' or 'b' button on your keyboard!")
        print("Моля натиснете 'e' или 'b' бутона на клавиатурата!")
        print("By pressing 'е' you will play the game in English. By pressing 'b' you will play the game in Bulgarian.")
        print("Натискайки 'e' ще играете играта на английски език. Натискайки 'b' ще играете играта на български език.")
        new_human_answer = input().strip()
        language = choose_language(new_human_answer)
        return language


def check_language(english_language, english, bulgarian):
    if english_language:
        print(english)
    else:
        print(bulgarian)
