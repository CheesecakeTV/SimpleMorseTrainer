import random
import string
from collections.abc import Iterable
from typing import Hashable

import SwiftGUI as sg

import constants
from morse import m_encode, m_decode
import globals

class Trainer(sg.BasePopupNonblocking):

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
                    key="user_in",
                    default_event=True,
                    justify="center",
                    fontsize=20,
                    width=10,
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

        super().__init__(layout, padx=30, pady=30)
        self.start_next_challenge()

    def get_challenge_text(
            self,
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


    ### Actions for the user-interface and/or control loop
    correct_solution: str | None = None
    def start_next_challenge(self):
        next_challenge = self.get_challenge_text()

        while next_challenge == self.correct_solution:
            next_challenge = self.get_challenge_text()

        self.correct_solution = next_challenge
        self.w["text"].value = m_encode(next_challenge)
        self.user_in.value = ""
        self.user_in.set_focus()

    def check_user_input(self) -> bool:
        """Check if the user entered correctly"""
        return self.user_in.value.upper() == self.correct_solution

    score_correct = 0
    score_errors = 0
    score_corrects_since_error = 0
    score_best_streak = 0
    def _event_loop(self, e: Hashable, v: sg.ValueDict):
        if e == "user_in":
            if self.check_user_input():
                self.start_next_challenge()
                self.score_correct += 1
                v["score_correct"] = self.score_correct
                self.user_in.update(background_color=constants.GREEN)
                self.score_corrects_since_error += 1
            else:
                self.user_in.value = ""
                self.score_errors += 1
                v["score_errors"] = self.score_errors
                self.user_in.update(background_color=constants.RED)
                self.score_corrects_since_error = 0

            v["score_accuracy"] = round(100 * self.score_correct / (self.score_correct + self.score_errors), 2)
            v["score_since_error"] = self.score_corrects_since_error

            if self.score_corrects_since_error > self.score_best_streak:
                self.score_best_streak = self.score_corrects_since_error
                v["score_best_streak"] = self.score_best_streak


