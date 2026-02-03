import SwiftGUI as sg
import trainers
from trainers import LetterToMorse, MorseToLetter, SingleLettersMixed, MorseToWord, MorseToString, MorseToSentence, LetterToNato


class MainMenu(sg.BasePopupNonblocking):
    def __init__(self):
        sg.GlobalOptions.Button.fontsize = 12
        sg.GlobalOptions.Common_Textual.fontsize = 12

        layout = [
            [
                sg.T("--/---/.-./.../.\n-/.-./.-/../-././.-.", justify= "center")
            ], [
                sg.Spacer(height=30)
            ],[
                self._make_button_group("Single letters", LetterToMorse, MorseToLetter, SingleLettersMixed)
            ],[
                sg.Spacer(height=8)
            ], [
                self._make_button_group("Words/Strings", MorseToWord, MorseToString)
            ],[
                sg.Spacer(height=8)
            ],[
                self._make_button_group("Sentences", MorseToSentence)
            ], [
                sg.Spacer(height=8)
            ], [
                self._make_button_group("NATO alphabet", LetterToNato)
            ]
        ]

        super().__init__(layout, title= "Morse Trainer", padx= 30, pady= 30)

    @staticmethod
    def _make_button(cls: type[trainers.BaseTrainer]) -> sg.Button:
        """Make a trainer-button from a trainer-class"""
        return sg.Button(
            cls.title,
            key_function= lambda: cls().w.block_others_until_close(),
            width= 26,
        )

    def _make_button_group(self, title: str, *classes: type[trainers.BaseTrainer]) -> sg.LabelFrame:
        """Make a whole label-frame with trainer-classes"""
        layout = [
            [self._make_button(cls)] for cls in classes
        ]

        return sg.LabelFrame(layout, text= title, padx=5, pady=5, fontsize= 14)


