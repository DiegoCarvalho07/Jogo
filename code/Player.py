#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame.key

from code.Const import ENTITY_SPEED, WIN_HEIGHT, WIN_WIDTH, PLAYER_KEY_UP, PLAYER_KEY_DOWN, PLAYER_KEY_LEFT, \
    PLAYER_KEY_RIGHT, PLAYER_KEY_ATTACK
from code.Entity import Entity


class Player(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self.invincible_timer = 45
        self.attack_cooldown = 10
        self.stun_timer = 10
        self.attack_lock_timer = 0

    def move(self):

        if self.attack_lock_timer > 0:
            self.attack_lock_timer -= 1

        if self.state != 'attack' and self.attacking:
            self.attacking = False

        if self.invincible_timer > 0:
            self.invincible_timer -= 1

        if self.dead:
            self.animate()
            return

        if self.hurt:
            self.animate()
            return

        if self.state == 'idle' and self.attacking:
            self.attacking = False

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

        if self.rect.left < 15:
           self.rect.left = 15

        if self.rect.right > 590:
           self.rect.right = 590

        if self.rect.top < 85:
           self.rect.top = 85

        if self.rect.bottom > WIN_HEIGHT:
           self.rect.bottom = WIN_HEIGHT

        self.attack()
        self.animate()

    def attack(self):

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        keys = pygame.key.get_pressed()

        if (
                keys[PLAYER_KEY_ATTACK]
                and not self.attacking
                and self.attack_cooldown == 0
        ):
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
                5,
                self.rect.height - 30
            )

        return pygame.Rect(
            self.rect.left - 5,
            self.rect.top + 15,
            5,
            self.rect.height - 30
        )
