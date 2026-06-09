#!/usr/bin/python
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from pydoc_data.topics import topics

import pygame
import os

from code.Const import ENTITY_HEALTH, ENTITY_DAMAGE, ENTITY_SCORE


class Entity(ABC):

    def __init__(self, name: str, position: tuple):

        self.health = None
        self.name = name
        self.dead = False

        self.animations = {
            'idle': self.load_animation(f'./asset/{name}/idle'),
            'walk': self.load_animation(f'./asset/{name}/walk'),
            'attack': self.load_animation(f'./asset/{name}/attack'),
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
        self.health = ENTITY_HEALTH[self.name]
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

                    frames.append(image)

        return frames

    def animate(self):


        frames = self.animations[self.state]

        self.frame += self.animation_speed

        if self.frame >= len(frames):

            if self.state == 'attack':
                self.attacking = False
                self.state = 'idle'

            elif self.state == 'death':
                self.frame = len(frames) - 1
                return

            else:
                self.frame = 0

        sprite = frames[int(self.frame)]

        if not self.facing_right:
            sprite = pygame.transform.flip(
                sprite,
                True,
                False
            )

        self.surf = sprite

    def take_damage(self, damage):

            self.health -= damage

            if self.health <= 0:
                self.dead = True
                self.state = 'death'
                self.frame = 0

    @abstractmethod
    def move(self):
        pass
