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

# Colors
GREEN = sg.Color.SpringGreen4
RED = sg.Color.OrangeRed3
