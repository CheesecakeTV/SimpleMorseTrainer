import SwiftGUI as sg
import menu

"""

Run this file as an entry-point to the program.

"""

if __name__ == '__main__':
    sg.Themes.FourColors.DarkGold()

    menu.MainMenu().w.loop()
