import SwiftGUI as sg

SHORT = "."
LONG = "-"
NEW_LETTER = "/"
NEW_WORD = " "
UNKNOWN = "?"

# You need to use . for short and - for long.
# It is replaced later.
LETTERS = {
    "a":".-",
    "b":"-...",
    "c":"-.-.",
    "d":"-..",
    "e":".",
    "f":"..-.",
    "g":"--.",
    "h":"....",
    "i":"..",
    "j":".---",
    "k":"-.-",
    "l":".-..",
    "m":"--",
    "n":"-.",
    "o":"---",
    "p":".--.",
    "q":"--.-",
    "r":".-.",
    "s":"...",
    "t":"-",
    "u":"..-",
    "v":"...-",
    "w":".--",
    "x":"-..-",
    "y":"-.--",
    "z":"--..",
}

LETTERS = {key:val.replace(".", SHORT).replace("-", LONG) for key,val in LETTERS.items()}

NATO_ALPHABET = {
    "a": "ALFA",
    "b": "BRAVO",
    "c": "CHARLIE",
    "d": "DELTA",
    "e": "ECHO",
    "f": "FOXTROT",
    "g": "GOLF",
    "h": "HOTEL",
    "i": "INDIA",
    "j": "JULIETT",
    "k": "KILO",
    "l": "LIMA",
    "m": "MIKE",
    "n": "NOVEMBER",
    "o": "OSCAR",
    "p": "PAPA",
    "q": "QUEBEC",
    "r": "ROMEO",
    "s": "SIERRA",
    "t": "TANGO",
    "u": "UNIFORM",
    "v": "VICTOR",
    "w": "WHISKEY",
    "x": "XRAY",
    "y": "YANKEE",
    "z": "ZULU",
}

GERMAN_ALPHABET = {
    "a": "ANTON",
    "ä": "ÄRGER",
    "b": "BERTA",
    "c": "CÄSAR",
    "ch": "CHARLOTTE",
    "d": "DORA",
    "e": "EMIL",
    "f": "FRIEDRICH",
    "g": "GUSTAV",
    "h": "HEINRICH",
    "i": "IDA",
    "j": "JULIUS",
    "k": "KAUFMANN",
    "l": "LUDWIG",
    "m": "MARTHA",
    "n": "NORDPOL",
    "o": "OTTO",
    "ö": "ÖKONOM",
    "p": "PAULA",
    "q": "QUELLE",
    "r": "RICHARD",
    "s": "SIEGFRIED",
    "sch": "SCHULE",
    "t": "THEODOR",
    "u": "ULRICH",
    "ü": "ÜBEL",
    "v": "VIKTOR",
    "w": "WILHELM",
    "x": "XANTHIPPE",
    "y": "YPSILON",
    "z": "ZEPPELIN",
}

# Colors
GREEN = sg.Color.SpringGreen4
RED = sg.Color.OrangeRed3
