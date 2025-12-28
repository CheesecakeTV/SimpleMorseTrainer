from collections.abc import Iterable
import constants
import globals

def m_encode(
        text: str | Iterable,
        translation_dict: dict = globals.all_chars,
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

def m_decode(text: str, translation_dict: dict = globals.all_chars_invers) -> str:
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

