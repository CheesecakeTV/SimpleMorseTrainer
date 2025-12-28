import SwiftGUI as sg
import trainers
from trainers import LetterToMorse, MorseToLetter, SingleLettersMixed


class MainMenu(sg.BasePopupNonblocking):
    def __init__(self):
        sg.GlobalOptions.Button.fontsize = 12

        layout = [
            [
                self._make_button_group("Single letters", LetterToMorse, MorseToLetter, SingleLettersMixed)
            ]
        ]

        super().__init__(layout, title= "Morse Trainer")

    @staticmethod
    def _make_button(cls: type[trainers.BaseTrainer]) -> sg.Button:
        """Make a trainer-button from a trainer-class"""
        return sg.Button(
            cls.title,
            key_function= lambda: cls().w.block_others_until_close(),
            width= 20,
        )

    def _make_button_group(self, title: str, *classes: type[trainers.BaseTrainer]) -> sg.LabelFrame:
        """Make a whole label-frame with trainer-classes"""
        layout = [
            [self._make_button(cls)] for cls in classes
        ]

        return sg.LabelFrame(layout, text= title, padx=5, pady=5, fontsize= 14)


