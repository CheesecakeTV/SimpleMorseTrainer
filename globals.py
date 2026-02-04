import constants
import SwiftGUI as sg

def invert_dict(in_dict: dict) -> dict:
    """
    Make keys values and values keys
    :param in_dict:
    :return:
    """
    return {val:key for key,val in in_dict.items()}

sg.Files.set_root("Simple Morse Trainer SwiftGUI")
translation_config = sg.Files.ConfigFile(sg.Files.root_path("Translation.ini"))

all_chars = dict()
all_chars_invers = dict()
nato_alphabet = dict()
german_alphabet = dict()

def refresh_translations():
    all_chars.update(translation_config.section("Morse letters", defaults=constants.LETTERS).to_dict())
    # all_chars = constants.LETTERS
    all_chars_invers.update(invert_dict(all_chars))

    nato_alphabet.update(translation_config.section("NATO alphabet", defaults=constants.NATO_ALPHABET).to_dict())
    german_alphabet.update(translation_config.section("German alphabet", defaults=constants.GERMAN_ALPHABET).to_dict())

refresh_translations()


