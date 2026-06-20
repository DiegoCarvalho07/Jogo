#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame.image
from pygame import Surface, Rect
from pygame.font import Font

from code.Const import WIN_WIDTH, C_ORANGE, MENU_OPTION, C_WHITE, C_YELLOW


class Menu:
    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load('./asset/throneroom.png').convert_alpha()
        self.rect = self.surf.get_rect(left=0, top=0)

    def run(self):
        menu_option = 0
        pygame.mixer_music.load('./asset/Menu.mp3')
        pygame.mixer_music.play(-1)
        while True:
            # DRAW IMAGES
            self.window.blit(source=self.surf, dest=self.rect)
            self.menu_text(65, "Fight  Arena", C_ORANGE, ((WIN_WIDTH / 2), 135))

            self.menu_text(17, "A", C_ORANGE, (30, 320))
            self.menu_text(17, "=LEFT", C_WHITE, (65, 320))

            self.menu_text(17, "D", C_ORANGE, (110, 320))
            self.menu_text(17, "=RIGHT", C_WHITE, (150, 320))

            self.menu_text(17, "W", C_ORANGE, (200, 320))
            self.menu_text(17, "=UP", C_WHITE, (230, 320))

            self.menu_text(17, "S", C_ORANGE, (260, 320))
            self.menu_text(17, "=DOWN", C_WHITE, (300, 320))

            self.menu_text(17, "L", C_ORANGE, (345, 320))
            self.menu_text(17, "=ATTACK", C_WHITE, (390, 320))

            self.menu_text(17, "RETURN", C_ORANGE, (470, 320))
            self.menu_text(17, "=ENTER", C_WHITE, (540, 320))


            for i in range(len(MENU_OPTION)):
                if i == menu_option:
                    self.menu_text(20, MENU_OPTION[i], C_YELLOW, ((WIN_WIDTH / 2), 200 + 25 * i))
                else:
                    self.menu_text(20, MENU_OPTION[i], C_WHITE, ((WIN_WIDTH / 2), 200 + 25 * i))
            pygame.display.flip()

            # Check for all events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  # Close Window
                    quit()  # end pygame
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:  # DOWN KEY
                        if menu_option < len(MENU_OPTION) - 1:
                            menu_option += 1
                        else:
                            menu_option = 0
                    if event.key == pygame.K_UP:  # UP KEY
                        if menu_option > 0:
                            menu_option -= 1
                        else:
                            menu_option = len(MENU_OPTION) - 1
                    if event.key == pygame.K_RETURN:  # ENTER
                        return MENU_OPTION[menu_option]

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="garamond", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)
