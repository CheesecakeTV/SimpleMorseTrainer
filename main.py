import SwiftGUI as sg
import trainers



if __name__ == '__main__':
    # sg.Examples.preview_all_themes(take_a_closer_look=trainers.Trainer)
    sg.Themes.FourColors.DarkGold()
    trainers.Trainer().w.loop()
