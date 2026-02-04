import SwiftGUI as sg

SHORT = "."
LONG = "-"
NEW_LETTER = "/"
NEW_WORD = " "
UNKNOWN = "?"

# You need to use . for short and - for long.
# It is replaced later.
LETTERS = {
    "A":".-",
    "B":"-...",
    "C":"-.-.",
    "D":"-..",
    "E":".",
    "F":"..-.",
    "G":"--.",
    "H":"....",
    "I":"..",
    "J":".---",
    "K":"-.-",
    "L":".-..",
    "M":"--",
    "N":"-.",
    "O":"---",
    "P":".--.",
    "Q":"--.-",
    "R":".-.",
    "S":"...",
    "T":"-",
    "U":"..-",
    "V":"...-",
    "W":".--",
    "X":"-..-",
    "Y":"-.--",
    "Z":"--..",
}

LETTERS = {key:val.replace(".", SHORT).replace("-", LONG) for key,val in LETTERS.items()}

NATO_ALPHABET = {
    "A": "ALFA",
    "B": "BRAVO",
    "C": "CHARLIE",
    "D": "DELTA",
    "E": "ECHO",
    "F": "FOXTROT",
    "G": "GOLF",
    "H": "HOTEL",
    "I": "INDIA",
    "J": "JULIETT",
    "K": "KILO",
    "L": "LIMA",
    "M": "MIKE",
    "N": "NOVEMBER",
    "O": "OSCAR",
    "P": "PAPA",
    "Q": "QUEBEC",
    "R": "ROMEO",
    "S": "SIERRA",
    "T": "TANGO",
    "U": "UNIFORM",
    "V": "VICTOR",
    "W": "WHISKEY",
    "X": "XRAY",
    "Y": "YANKEE",
    "Z": "ZULU",
}

GERMAN_ALPHABET = {
    "A": "ANTON",
    "Ä": "ÄRGER",
    "B": "BERTA",
    "C": "CÄSAR",
    "CH": "CHARLOTTE",
    "D": "DORA",
    "E": "EMIL",
    "F": "FRIEDRICH",
    "G": "GUSTAV",
    "H": "HEINRICH",
    "I": "IDA",
    "J": "JULIUS",
    "K": "KAUFMANN",
    "L": "LUDWIG",
    "M": "MARTHA",
    "N": "NORDPOL",
    "O": "OTTO",
    "Ö": "ÖKONOM",
    "P": "PAULA",
    "Q": "QUELLE",
    "R": "RICHARD",
    "S": "SIEGFRIED",
    "SCH": "SCHULE",
    "T": "THEODOR",
    "U": "ULRICH",
    "Ü": "ÜBEL",
    "V": "VIKTOR",
    "W": "WILHELM",
    "X": "XANTHIPPE",
    "Y": "YPSILON",
    "Z": "ZEPPELIN",
}

# Colors
GREEN = sg.Color.SpringGreen4
RED = sg.Color.OrangeRed3
