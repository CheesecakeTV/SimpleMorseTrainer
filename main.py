from collections.abc import Iterable
import string
import SwiftGUI as sg
import random
import constants

sg.Themes.FourColors.DarkGold()

_GREEN = sg.Color.SpringGreen4
_RED = sg.Color.OrangeRed3

all_chars = constants.LETTERS
all_chars_invers = {val:key for key,val in all_chars.items()}

def m_encode(
        text: str | Iterable,
        translation_dict: dict = all_chars,
        join_str: str = constants.NEW_LETTER,
) -> str:
    """
    Convert a clear text to morse code
    :param join_str:
    :param translation_dict:
    :param text: Text to encode
    :return: Clear text, Morse
    """
    # Todo: This works only for single words atm
    return join_str.join(tuple(map(
        lambda s:translation_dict.get(s, constants.UNKNOWN),
        text,
    )))

def m_decode(text: str, translation_dict: dict = all_chars_invers) -> str:
    """

    :param text:
    :param translation_dict:
    :return:
    """
    words = text.split(constants.NEW_WORD)
    decoded = map(
        lambda s:m_encode(
            s.split(constants.NEW_LETTER),
            translation_dict= translation_dict,
            join_str= ""
        ),
        words
    )
    return " ".join(decoded)

def get_challenge_text(
        letter_count: int = 1,
        included_letters: Iterable[str] = string.ascii_uppercase,
) -> str:
    """
    Create a random clear text
    :param included_letters: These need to be uppercase!
    :param letter_count:
    :return:
    """
    return "".join(random.choices(included_letters, k=letter_count))

layout_score = [
    [
        sg.T("Correct: ", width=18),
        sg.T("0", key="score_correct"),
    ], [
        sg.T("Errors: ", width=18),
        sg.T("0", key="score_errors"),
    ], [
        sg.T("Accuracy: ", width=18),
        sg.T("-", key="score_accuracy", width= 5),
        sg.T("%")
    ], [
        sg.T("Streak: ", width=18),
        sg.T("0", key="score_since_error"),
    ], [
        sg.T("Best streak: ", width=18),
        sg.T("0", key="score_best_streak"),
    ]
]

layout = [
    [
        sg.T(
            "",
            key= "text",
            fontsize= 20,
        )
    ],[
        sg.Spacer(height=30),
    ],[
        user_in := sg.In(
            key= "user_in",
            default_event= True,
            justify= "center",
            fontsize= 20,
            width= 10,
        )
    ],[
        sg.Spacer(height=10),
    ],[
        sg.HSep()
    ],[
        sg.Spacer(height=10),
    ],[
        sg.Frame(layout_score, alignment= "left")
    ]
]

### Actions for the user-interface and/or control loop
correct_solution: str | None = None
def start_next_challenge():
    global correct_solution

    next_challenge = get_challenge_text()

    while next_challenge == correct_solution:
        next_challenge = get_challenge_text()

    correct_solution = next_challenge
    w["text"].value = m_encode(correct_solution)
    user_in.value = ""
    user_in.set_focus()

def check_user_input() -> bool:
    """Check if the user entered correctly"""
    return user_in.value.upper() == correct_solution

score_correct = 0
score_errors = 0
score_corrects_since_error = 0
score_best_streak = 0

w = sg.Window(layout, title="Morse code trainer", padx=30, pady=30, keep_on_top= True)
start_next_challenge()

for e,v in w:

    if e == "user_in":
        if check_user_input():
            start_next_challenge()
            score_correct += 1
            v["score_correct"] = score_correct
            user_in.update(background_color = _GREEN)
            score_corrects_since_error += 1
        else:
            user_in.value = ""
            score_errors += 1
            v["score_errors"] = score_errors
            user_in.update(background_color = _RED)
            score_corrects_since_error = 0

        v["score_accuracy"] = round(100 * score_correct / (score_correct + score_errors), 2)
        v["score_since_error"] = score_corrects_since_error

        if score_corrects_since_error > score_best_streak:
            score_best_streak = score_corrects_since_error
            v["score_best_streak"] = score_best_streak

