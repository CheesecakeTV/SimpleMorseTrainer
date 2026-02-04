import SwiftGUI as sg
import trainers
from trainers import LetterToMorse, MorseToLetter, SingleLettersMixed, MorseToWord, MorseToString, MorseToSentence, LetterToNato, LetterToGermanAlphabet
import globals

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
                self._make_button_group("Spelling alphabet", LetterToNato, LetterToGermanAlphabet)
            ],[
                sg.Spacer(height=16)
            ],[
                sg.LabelFrame(
                    [[self._make_configuration_button(section)] for _,section in globals.translation_config.all_sections.items()],
                    text= "Configure translation",
                    padx=5,
                    pady=5,
                    fontsize= 14,
                )
            ]
        ]

        super().__init__(layout, title= "Morse Trainer", padx= 30, pady= 30)

    @staticmethod
    def _make_configuration_button(section: sg.Files.ConfigSection) -> sg.Button:
        """Make a button to configure translation configuration"""
        return sg.Button(
            section.section.name,
            key_function= [
                lambda: sg.Files.ConfigSectionEditor(section).popup(title= section.section.name),
                globals.refresh_translations,
            ],
            expand= True,
            width= 26,
        )

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


