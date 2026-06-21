#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import random
import sys

from pygame import Surface, Rect
from pygame.font import Font

from code.Const import (
    C_WHITE,
    C_GREEN,
    EVENT_ENEMY,
    EVENT_TIMEOUT,
    SPAWN_TIME,
    TIMEOUT_STEP,
    TIMEOUT_LEVEL, WIN_WIDTH
)

from code.Entity import Entity
from code.EntityFactory import EntityFactory
from code.EntityMediator import EntityMediator
from code.Player import Player


class Level:

    def __init__(self, window: Surface, name: str, player_score: int):

        self.timeout = TIMEOUT_LEVEL
        self.window = window
        self.name = name
        self.enemies_spawned = 0
        self.enemies_killed = 0
        self.max_enemies = 8

        self.entity_list: list[Entity] = []

        self.background = pygame.image.load(
            f'./asset/{self.name}.png'
        ).convert_alpha()

        player = EntityFactory.get_entity('Player')
        player.score = player_score

        self.entity_list.append(player)

        pygame.time.set_timer(
            EVENT_ENEMY,
            SPAWN_TIME
        )

        pygame.time.set_timer(
            EVENT_TIMEOUT,
            TIMEOUT_STEP
        )

    def run(self, player_score: int):

        pygame.mixer_music.load(
            f'./asset/{self.name}.mp3'
        )

        pygame.mixer_music.set_volume(0.3)
        pygame.mixer_music.play(-1)

        clock = pygame.time.Clock()

        while True:

            clock.tick(60)

            self.window.blit(
                self.background,
                (0, 0)
            )

            player_dead = False

            for ent in self.entity_list:
                if isinstance(ent, Player):
                    player_dead = ent.dead
                    break

            # move e desenha entidades
            for ent in self.entity_list:

                ent.move()

                self.window.blit(
                    source=ent.surf,
                    dest=ent.rect
                )

                self.draw_health_bar(ent)

                if isinstance(ent, Player):

                    self.level_text(
                        14,
                        f'Score: {ent.score}',
                        C_GREEN,
                        (10, 25))
                    self.level_text(
                        14,
                        f'Kills: {self.enemies_killed}/{self.max_enemies}',
                        C_GREEN,
                        (10, 45)
                    )


            # eventos
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == EVENT_ENEMY:

                    enemy_count = sum(
                        1 for ent in self.entity_list
                        if ent.name.startswith('Enemy')
                    )

                    if enemy_count >= 2:
                        continue

                    if self.enemies_spawned >= self.max_enemies:
                        continue

                    choice = random.choice(
                        ('Enemy1', 'Enemy2')
                    )

                    enemy = EntityFactory.get_entity(
                        choice
                    )

                    self.enemies_spawned += 1

                    for ent in self.entity_list:
                        if isinstance(ent, Player):
                            enemy.target = ent
                            break

                    self.entity_list.append(enemy)

                if event.type == EVENT_TIMEOUT:

                    self.timeout -= TIMEOUT_STEP

                    if self.timeout <= 0:

                        if self.enemies_killed < self.max_enemies:

                            self.level_text(
                                40,
                                'YOU LOST,TIME OUT',
                                (255, 0, 0),
                                (100, 130)
                            )

                            self.level_text(
                                18,
                                f'Enemies defeated: {self.enemies_killed}/{self.max_enemies}',
                                C_WHITE,
                                (180, 190)
                            )

                            pygame.display.flip()
                            pygame.time.delay(5000)

                            return False

                        else:

                            for ent in self.entity_list:
                                if isinstance(ent, Player):
                                    return ent.score

            # GAME OVER
            if player_dead:

                self.level_text(
                    40,
                    'GAME OVER',
                    (255, 0, 0),
                    (190, 110)
                )

                self.level_text(
                    20,
                    'Your warrior has fallen',
                    C_WHITE,
                    (160, 170)
                )

                pygame.display.flip()

                pygame.time.delay(5000)

                return False

            if (self.enemies_killed >= self.max_enemies):
                self.level_text(40,'LEVEL COMPLETED',(0,255,0),(120,140))
                pygame.display.flip()
                pygame.time.delay(3000)

                for ent in self.entity_list:
                    if isinstance(ent, Player):
                        return ent.score

            # se não houver player
            if not any(
                isinstance(ent, Player)
                for ent in self.entity_list
            ):
                return False

            # texto do tempo
            self.level_text(
                14,
                f'{self.name} - Timeout: {self.timeout / 1000:.1f}s',
                C_WHITE,
                (10, 5)
            )

            # colisões
            EntityMediator.verify_collision(
                entity_list=self.entity_list
            )

            # mortes
            self.enemies_killed += EntityMediator.verify_health(
                entity_list=self.entity_list
            )

            pygame.display.flip()

    def level_text(
            self,
            text_size: int,
            text: str,
            text_color: tuple,
            text_pos: tuple
    ):

        text_font: Font = pygame.font.SysFont(
            name="Lucida Sans Typewriter",
            size=text_size
        )

        text_surf: Surface = text_font.render(
            text,
            True,
            text_color
        ).convert_alpha()

        text_rect: Rect = text_surf.get_rect(
            left=text_pos[0],
            top=text_pos[1]
        )

        self.window.blit(
            source=text_surf,
            dest=text_rect
        )

    def draw_health_bar(self, ent):

        width = ent.rect.width
        height = 5

        current_width = max(
            0,
            int(
                (ent.health / ent.max_health)
                * width
            )
        )

        # fundo vermelho
        pygame.draw.rect(
            self.window,
            (255, 0, 0),
            (
                ent.rect.left,
                ent.rect.top - 10,
                width,
                height
            )
        )

        # vida verde
        pygame.draw.rect(
            self.window,
            (0, 255, 0),
            (
                ent.rect.left,
                ent.rect.top - 10,
                current_width,
                height
            )
        )
        