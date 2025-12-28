import random
from abc import abstractmethod

import SwiftGUI as sg

import constants
from morse import m_encode, m_decode
import globals

class BaseTrainer(sg.BasePopupNonblocking):
    title: str = ""

    def __init__(self):
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
                    fontsize=20,
                )
            ], [
                sg.Spacer(height=30),
            ], [
                user_in := sg.In(
                    key_function= self.input_changed,
                    default_event=True,
                    justify="center",
                    fontsize=20,
                    width=10,
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
            ]
        ]
        self.user_in = user_in

        super().__init__(layout, padx=30, pady=30, title= self.title, keep_on_top= True)
        self.start_next_challenge()

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

        while next_solution == self.correct_solution:
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

    def process_input(self):
        """This should be called when the user-input is done"""
        correct = self.check_user_input()

        if correct:
            self.start_next_challenge()
        else:
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
    def update_score(self, correct: bool):
        """Update the score"""
        v = self.w.value

        if correct:
            self.score_correct += 1
            v["score_correct"] = self.score_correct
            self.user_in.update(background_color=constants.GREEN)
            self.score_corrects_since_error += 1
        else:
            self.score_errors += 1
            v["score_errors"] = self.score_errors
            self.user_in.update(background_color=constants.RED)
            self.score_corrects_since_error = 0

        v["score_accuracy"] = round(100 * self.score_correct / (self.score_correct + self.score_errors), 2)
        v["score_since_error"] = self.score_corrects_since_error

        if self.score_corrects_since_error > self.score_best_streak:
            self.score_best_streak = self.score_corrects_since_error
            v["score_best_streak"] = self.score_best_streak

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
