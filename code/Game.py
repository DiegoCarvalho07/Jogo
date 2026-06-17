#!/usr/bin/python
# -*- coding: utf-8 -*-


import pygame

from code.Const import WIN_WIDTH, WIN_HEIGHT, MENU_OPTION
from code.Level import Level
from code.Menu import Menu
from code.Score import Score


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))

    def run(self):
        while True:
            score = Score(self.window)
            menu = Menu(self.window)
            menu_return = menu.run()

            if menu_return == MENU_OPTION[0]:
                player_score = 0

                level = Level(self.window, 'Level1', player_score)
                result = level.run(player_score)

                if result is False:
                    continue

                player_score = result

                level = Level(self.window, 'Level2', player_score)
                result = level.run(player_score)

                if result is False:
                    continue

                player_score = result
                score.save(player_score)

            elif menu_return == MENU_OPTION[1]:
                score.show()
            elif menu_return == MENU_OPTION[2]:
                pygame.quit()  # Close Window
                quit()  # end pygame
            else:
                pygame.quit()
                sys.exit()
