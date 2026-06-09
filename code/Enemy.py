#!/usr/bin/python
# -*- coding: utf-8 -*-
from code.Const import ENTITY_SPEED
from code.Entity import Entity


class Enemy(Entity):

    def __init__(self, name, position):
        super().__init__(name, position)

        self.state = 'walk'
        self.facing_right = False

    def move(self):

        self.rect.centerx -= ENTITY_SPEED[self.name]

        self.state = 'walk'

        self.animate()

    def move(self):
        self.rect.centerx -= ENTITY_SPEED[self.name]

    def shoot(self):
        self.shot_delay -= 1
        if self.shot_delay == 0:
            self.shot_delay = ENTITY_SHOT_DELAY[self.name]
            return EnemyShot(name=f'{self.name}Shot', position=(self.rect.centerx, self.rect.centery))
