import random
from abc import abstractmethod
import SwiftGUI as sg
import constants
from morse import m_encode, m_decode
import globals

from textgeneration import word_generator, sentence_generator


class BaseTrainer(sg.BasePopupNonblocking):
    title: str = ""
    input_fontsize: int = 18

    def __init__(self):
        layout = self._get_layout()

        super().__init__(layout, padx=30, pady=30, title= self.title, keep_on_top= True, grab_anywhere= True)
        self.start_next_challenge()

    user_in: sg.Input   # The input-element for the user
    def _get_layout(self) -> list[list[sg.BaseElement]]:
        layout_score = [
            [
                sg.T("Correct: ", width=18),
                sg.T("0", key="score_correct"),
            ], [
                sg.T("Errors: ", width=18),
                sg.T("0", key="score_errors"),
            ], [
                sg.T("Accuracy: ", width=18),
                sg.T("-", key="score_accuracy", width=5),
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
                    key="text",
                    fontsize=self.input_fontsize,
                )
            ], [
                sg.Spacer(height=30),
            ], [
                user_in := sg.In(
                    key_function= self.input_changed,
                    default_event=True,
                    justify="center",
                    fontsize=16,
                    width=10,
                    expand= True
                ).bind_event(
                    sg.Event.KeyEnter,
                    key_function= self.input_return,
                )
            ], [
                sg.Spacer(height=10),
            ], [
                sg.HSep()
            ], [
                sg.Spacer(height=10),
            ], [
                sg.Frame(layout_score, alignment="left")
            ], [
                sg.Spacer(height= 10)
            ], [
                sg.HSep()
            ], [
                sg.Spacer(height= 10)
            ], [
                sg.Button("Skip (+1 error)", key_function= self.skip)
            ]
        ]
        self.user_in: sg.Input = user_in

        return layout

    @abstractmethod
    def get_next_challenge(self) -> tuple[str, str]:
        """
        Return the next challenge and its correct solution.
        :return: Challenge, Solution
        """
        ...

    ### Actions for the user-interface and/or control loop
    correct_solution: str | None = None
    def start_next_challenge(self):
        """Set up and start the next challenge"""
        next_challenge, next_solution = self.get_next_challenge()

        while constants.UNKNOWN in next_challenge or next_solution == self.correct_solution:
            # If the same problem occurs twice in a row, redo the challenge
            self.start_next_challenge()
            return

        self.correct_solution = next_solution
        self.w["text"].value = next_challenge
        self.user_in.value = ""
        self.user_in.set_focus()

    def check_user_input(self) -> bool:
        """Check if the user entered correctly"""
        return self.user_in.value.strip().upper() == self.correct_solution

    def process_input(self, clear_if_wrong: bool = True):
        """This should be called when the user-input is done"""
        correct = self.check_user_input()

        if correct:
            self.start_next_challenge()
        elif clear_if_wrong:
            self.user_in.value = ""

        self.update_score(correct)

    def input_changed(self):
        """Called when the input changed"""
        self.process_input()

    def input_return(self):
        """Called when the user presses enter/return in the input-bar"""
        self.process_input()

    score_correct = 0
    score_errors = 0
    score_corrects_since_error = 0
    score_best_streak = 0
    had_an_error_on_this = False    # True, if there already was an error on this challenge
    def update_score(self, correct: bool):
        """Update the score"""
        v = self.w.value

        if correct:
            self.had_an_error_on_this = False
            self.score_correct += 1
            v["score_correct"] = self.score_correct
            self.user_in.update(background_color=constants.GREEN)
            self.score_corrects_since_error += 1
        elif self.had_an_error_on_this:
            self.user_in.update(background_color=constants.RED)
            return
        else:
            self.had_an_error_on_this = True    # Don't count the error twice
            self.score_errors += 1
            v["score_errors"] = self.score_errors
            self.user_in.update(background_color=constants.RED)
            self.score_corrects_since_error = 0

        v["score_accuracy"] = round(100 * self.score_correct / (self.score_correct + self.score_errors), 2)
        v["score_since_error"] = self.score_corrects_since_error

        if self.score_corrects_since_error > self.score_best_streak:
            self.score_best_streak = self.score_corrects_since_error
            v["score_best_streak"] = self.score_best_streak

    def skip(self):
        """Skip the current challenge and add an error"""
        self.update_score(correct= False)
        self.had_an_error_on_this = False

        self.start_next_challenge()

class MorseToLetter(BaseTrainer):
    title = "Morse to letter"

    def get_next_challenge(self) -> tuple[str, str]:
        included_letters = globals.all_chars.keys()
        letter_count = 1

        clear_text = "".join(random.choices(list(included_letters), k=letter_count))

        return m_encode(clear_text, translation_dict= globals.all_chars), clear_text

class LetterToMorse(MorseToLetter):
    title = "Letter to morse"

    def __init__(self):
        super().__init__()
        self.user_in.bind_event("<space>", key_function= self.input_return)

    def get_next_challenge(self) -> tuple[str, str]:
        solution, challenge = super().get_next_challenge() # Switch challenge and solution
        return challenge, solution

    def input_changed(self):
        pass    # Deactivate instant check if input is correct

class SingleLettersMixed(MorseToLetter):
    title = "Mixed"

    morse_to_letter_mode: bool = False  # True, if a morse-string is converted to a letter at the moment
    def get_next_challenge(self) -> tuple[str, str]:
        self.morse_to_letter_mode = random.choice([True, False])

        challenge, solution = super().get_next_challenge()

        if self.morse_to_letter_mode:
            return challenge, solution
        else:
            return solution, challenge

    def input_changed(self):
        if self.morse_to_letter_mode:
            super().input_changed()
        else:
            pass    # Input should do nothing when not in morse-to-letter-mode

class MorseToWord(BaseTrainer):
    title = "Morse to word"
    input_fontsize = 12

    translation_dict: dict = {   # Add/modify the translation-dict when encoding text
        " ": " ",   # Space should stay space
    }

    def __init__(self):
        temp = globals.all_chars.copy() # Add custom chars
        temp.update(self.translation_dict)
        self.translation_dict = temp

        super().__init__()

    def generate_challenge_text(self) -> str:
        """Generate the word/sentence to input"""
        return word_generator.word(
            include_categories=["nouns"],
            word_min_length=self.len_min,
            word_max_length=self.len_max,
            exclude_with_spaces= True,
        )

    def get_next_challenge(self) -> tuple[str, str]:
        clear_text = self.generate_challenge_text().upper()
        return m_encode(clear_text, translation_dict= self.translation_dict), clear_text

    def process_input(self, clear_if_wrong: bool = False):  # Overwritten to not clear the input by default
        super().process_input(clear_if_wrong= clear_if_wrong)

    def input_changed(self, strip:bool = True):
        user_input = self.user_in.value
        if strip:
            user_input = user_input.strip()

        if len(self.correct_solution) <= len(user_input):
            super().input_changed()
        elif not self.had_an_error_on_this:
            self.user_in.update_to_default_value("background_color")

    def _update_wordlength(self, w: sg.Window, e: str = None, val: float = 0):
        if e == "len_max":
            self.len_max = int(val)
            w["len_min"].update(number_max= val)
        elif e == "len_min":
            self.len_min = int(val)
            w["len_max"].update(number_min= val)

    len_min: int = 4
    len_max: int = 8
    def _get_layout(self) -> list[list[sg.BaseElement]]:
        layout = super()._get_layout()

        layout_word_lengths = [
            [
                sg.T("Length (character count)")
            ],
            [
                sg.T("Min: "),
                sg.Scale(
                    number_min= 2,
                    number_max= self.len_max,
                    default_value=self.len_min,
                    key="len_min",
                    default_event=True,
                    key_function= self._update_wordlength,
                )
            ],[
                sg.T("Max: "),
                sg.Scale(
                    number_min=self.len_min,
                    number_max=17,
                    default_value=self.len_max,
                    key= "len_max",
                    default_event= True,
                    key_function=self._update_wordlength,
                )
            ]
        ]

        layout += [
            [
                sg.Spacer(height= 10),
            ],
            [
                sg.HSep()
            ],[
                sg.Frame(layout_word_lengths)
            ]
        ]

        return layout

class MorseToString(MorseToWord):
    title = "Morse to string"

    def generate_challenge_text(self) -> str:
        included_letters = globals.all_chars.keys()
        letter_count = random.randint(self.len_min, self.len_max)

        clear_text = "".join(random.choices(list(included_letters), k=letter_count))

        return clear_text

class MorseToSentence(MorseToWord):
    title = "Morse to Sentence"

    def generate_challenge_text(self) -> str:
        text = sentence_generator.sentence().replace(".", "")
        print(text)
        return text

    def _get_layout(self) -> list[list[sg.BaseElement]]:
        return super(MorseToWord, self)._get_layout()

