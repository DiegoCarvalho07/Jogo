#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame.key

from code.Const import ENTITY_SPEED, WIN_HEIGHT, WIN_WIDTH, PLAYER_KEY_UP, PLAYER_KEY_DOWN, PLAYER_KEY_LEFT, \
    PLAYER_KEY_RIGHT, PLAYER_KEY_SHOOT, ENTITY_SHOT_DELAY
from code.Entity import Entity
from code.PlayerShot import PlayerShot


class Player(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self.health = 300
        self.shot_delay = ENTITY_SHOT_DELAY[self.name]

    def move(self):

            pressed_key = pygame.key.get_pressed()

            if self.attacking:
                self.animate()
                return

            moving = False

            if pressed_key[PLAYER_KEY_UP]:
                self.rect.centery -= ENTITY_SPEED[self.name]
                moving = True

            if pressed_key[PLAYER_KEY_DOWN]:
                self.rect.centery += ENTITY_SPEED[self.name]
                moving = True

            if pressed_key[PLAYER_KEY_LEFT]:
                self.rect.centerx -= ENTITY_SPEED[self.name]
                self.facing_right = False
                moving = True

            if pressed_key[PLAYER_KEY_RIGHT]:
                self.rect.centerx += ENTITY_SPEED[self.name]
                self.facing_right = True
                moving = True

            if moving:
                self.state = 'walk'
            else:
                self.state = 'idle'

            if self.rect.left < 50:
                self.rect.left = 50

            if self.rect.right > 560:
                self.rect.right = 560

            if self.rect.top < 70:
                self.rect.top = 70

            if self.rect.bottom > WIN_HEIGHT:
                self.rect.bottom = WIN_HEIGHT

            self.animate()

    def shoot(self):
        self.shot_delay -= 1

        if self.shot_delay == 0:
            self.shot_delay = ENTITY_SHOT_DELAY[self.name]
            pressed_key = pygame.key.get_pressed()

            if pressed_key[PLAYER_KEY_SHOOT]:
                self.attaking = True
                self.state = 'attack'
                self.frame = 0

                return PlayerShot(
                    name=f'{self.name} Shot',
                    position=(self.rect.centerx,self.rect.centery )
                )
            return None
