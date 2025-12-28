import SwiftGUI as sg
import trainers
import menu


if __name__ == '__main__':
    # sg.Examples.preview_all_themes(take_a_closer_look=trainers.Trainer)
    sg.Themes.FourColors.DarkGold()
    #trainers.MorseToLetter().w.loop()
    #trainers.LetterToMorse()#.w.loop()

    menu.MainMenu().w.loop()
