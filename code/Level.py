# !/usr/bin/python
# -*- coding: utf-8 -*-
import random
import sys

import pygame
from pygame import Surface, Rect
from pygame.font import Font

from code.Const import C_WHITE, WIN_HEIGHT, EVENT_ENEMY, SPAWN_TIME, C_GREEN, C_CYAN, EVENT_TIMEOUT, \
    TIMEOUT_STEP, TIMEOUT_LEVEL
from code.Enemy import Enemy
from code.Entity import Entity
from code.EntityFactory import EntityFactory
from code.EntityMediator import EntityMediator
from code.Player import Player


class Level:
    def __init__(self, window: Surface, name: str, player_score: int):
        self.timeout = TIMEOUT_LEVEL
        self.window = window
        self.name = name
        self.entity_list: list[Entity] = []
        self.background = pygame.image.load(f'./asset/{self.name}.png').convert_alpha()
        player = EntityFactory.get_entity('Player')
        player.score = player_score
        self.entity_list.append(player)
        pygame.time.set_timer(EVENT_ENEMY, SPAWN_TIME)
        pygame.time.set_timer(EVENT_TIMEOUT, TIMEOUT_STEP)  # 100ms

    def run(self, player_score: int):
        pygame.mixer_music.load(f'./asset/{self.name}.mp3')
        pygame.mixer_music.set_volume(0.3)
        pygame.mixer_music.play(-1)
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            self.window.blit(self.background, (0, 0))
            for ent in self.entity_list:
                self.window.blit(source=ent.surf, dest=ent.rect)
                self.draw_health_bar(ent)
                
                if isinstance(ent, Player):
                    pygame.draw.rect(
                        self.window,
                        (255, 0, 0),
                        ent.get_attack_rect(),
                        2
                    )
                ent.move()
                if isinstance(ent, Player):
                    self.level_text(14, f'Player - Health: {ent.health} | Score: {ent.score}', C_GREEN, (10, 25))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == EVENT_ENEMY:

                    choice = random.choice(
                        ('Enemy1', 'Enemy2')
                    )

                    enemy = EntityFactory.get_entity(choice)

                    for ent in self.entity_list:
                        if isinstance(ent, Player):
                            enemy.target = ent
                            break

                    self.entity_list.append(enemy)
                if event.type == EVENT_TIMEOUT:
                    self.timeout -= TIMEOUT_STEP
                    if self.timeout == 0:
                        for ent in self.entity_list:
                            if isinstance(ent, Player):
                                return ent.score

                if not any(isinstance(ent, Player) for ent in self.entity_list):
                    return False

            # printed text
            self.level_text(14, f'{self.name} - Timeout: {self.timeout / 1000:.1f}s', C_WHITE, (10, 5))
            
            pygame.display.flip()
            # Collisions
            EntityMediator.verify_collision(entity_list=self.entity_list)
            EntityMediator.verify_health(entity_list=self.entity_list)

    def level_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(left=text_pos[0], top=text_pos[1])
        self.window.blit(source=text_surf, dest=text_rect)

    def draw_health_bar(self, ent):

        width = 50
        height = 5

        current_width = max(
            0,
            int((ent.health / ent.max_health) * width)
        )

        # fundo vermelho
        pygame.draw.rect(
            self.window,
            (255, 0, 0),
            (ent.rect.left, ent.rect.top - 10, width, height)
        )

        # vida verde
        pygame.draw.rect(
            self.window,
            (0, 255, 0),
            (ent.rect.left, ent.rect.top - 10, current_width, height)
        )