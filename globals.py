import constants

def invert_dict(in_dict: dict) -> dict:
    """
    Make keys values and values keys
    :param in_dict:
    :return:
    """
    return {val:key for key,val in in_dict.items()}

all_chars = constants.LETTERS
all_chars_invers = invert_dict(all_chars)

nato_alphabet = constants.NATO_ALPHABET

