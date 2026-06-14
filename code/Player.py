#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame.key

from code.Const import ENTITY_SPEED, WIN_HEIGHT, WIN_WIDTH, PLAYER_KEY_UP, PLAYER_KEY_DOWN, PLAYER_KEY_LEFT, \
    PLAYER_KEY_RIGHT, PLAYER_KEY_ATTACK
from code.Entity import Entity


class Player(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self.health = 300


    def move(self):

        if self.dead:
            self.animate()
            return

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

        self.attack()
        self.animate()

    def attack(self):
        keys = pygame.key.get_pressed()

        if keys[PLAYER_KEY_ATTACK] and not self.attacking:
            self.attacking = True
            self.hit_registered = False
            self.state = 'attack'
            self.frame = 0

    def get_attack_rect(self):

        attack_height = 40
        attack_y = self.rect.centery - attack_height // 2

        if self.facing_right:
            return pygame.Rect(
                self.rect.right,
                self.rect.top + 15,
                35,
                self.rect.height - 30
            )

        return pygame.Rect(
            self.rect.left - 20,
            self.rect.top,
            20,
            self.rect.height
        )
