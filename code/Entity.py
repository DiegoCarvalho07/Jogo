#!/usr/bin/python
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

import pygame
import os

from code.Const import ENTITY_HEALTH, ENTITY_DAMAGE, ENTITY_SCORE, ENTITY_SCALE


class Entity(ABC):

    player_under_attack = False

    def __init__(self, name: str, position: tuple):

        self.name = name
        self.hurt = False
        self.stun_timer = 0
        self.invincible_timer = 0
        self.attack_cooldown = 0
        self.dead = False
        self.dying = False
        self.death_timer = 0
        self.hit_registered = False
        self.score_given = False
        self.max_health = ENTITY_HEALTH[self.name]
        self.health = self.max_health
        self.animations = {
            'idle': self.load_animation(f'./asset/{name}/idle'),
            'walk': self.load_animation(f'./asset/{name}/walk'),
            'attack': self.load_animation(f'./asset/{name}/attack'),
            'hurt': self.load_animation(f'./asset/{name}/hurt'),
            'death': self.load_animation(f'./asset/{name}/death')
        }

        self.state = 'idle'
        self.frame = 0
        self.animation_speed = 0.20

        self.surf = self.animations['idle'][0]

        self.rect = self.surf.get_rect(
            left=position[0],
            top=position[1])

        self.facing_right = True
        self.attacking = False
        self.damage = ENTITY_DAMAGE[self.name]
        self.score = ENTITY_SCORE[self.name]
        self.last_dmg = 'None'


    def load_animation(self, path):

        frames = []

        if os.path.exists(path):

            for file in sorted(os.listdir(path)):
                if file.endswith('.png'):
                    image = pygame.image.load(
                        os.path.join(path, file)
                    ).convert_alpha()

                    image = pygame.transform.scale(
                        image,
                        (
                            int(image.get_width() * ENTITY_SCALE),
                            int(image.get_height() * ENTITY_SCALE)
                        )
                    )

                    frames.append(image)
        return frames

    def animate(self):

        frames = self.animations[self.state]

        self.frame += self.animation_speed

        if self.frame >= len(frames):

            if self.state == 'attack':
                self.attacking = False
                self.state = 'idle'
                self.frame = 0

                Entity.player_under_attack = False

            elif self.state == 'hurt':

                self.hurt = False

                if self.dying:

                    self.dying = False
                    self.dead = True

                    self.state = 'death'
                    self.frame = 0
                    self.death_timer = 120

                else:

                    self.state = 'idle'
                    self.frame = 0


            elif self.state == 'death':

                if self.frame >= len(frames):
                    self.frame = len(frames) - 1

                sprite = frames[int(self.frame)]

                if not self.facing_right:
                    sprite = pygame.transform.flip(sprite, True, False)

                self.surf = sprite

                return

            else:
                self.frame = 0

            frames = self.animations[self.state]

        sprite = frames[int(self.frame)]

        if not self.facing_right:
            sprite = pygame.transform.flip(
                sprite,
                True,
                False
            )

        self.surf = sprite

    def take_damage(self, damage):

        if self.dead:
            return

        if self.invincible_timer > 0:
            return

        if self.name == 'Player':
            self.invincible_timer = 45
        else:
            self.invincible_timer = 15

        self.health -= damage

        if self.health <= 0:

            self.health = 0
            self.attacking = False
            self.hit_registered = False
            self.dying = True
            self.hurt = True
            self.state = 'hurt'
            self.frame = 0

        else:

            self.attacking = False
            self.hit_registered = False
            self.hurt = True

            if self.name == 'Player':
                self.attack_cooldown = 20
                self.stun_timer = 15
            else:
                self.attack_cooldown = 60
                self.stun_timer = 60

            if self.name == 'Enemy1':
                self.attack_cooldown = 15
                self.stun_timer = 10

            if self.name == 'Enemy2':
                self.attack_cooldown = 25
                self.stun_timer = 15

            self.state = 'hurt'
            self.frame = 0
    @abstractmethod
    def move(self):
        pass
