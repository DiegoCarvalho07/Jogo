from code.Const import ENTITY_SPEED
from code.Entity import Entity


class Enemy(Entity):

    def __init__(self, name, position):
        super().__init__(name, position)

        self.state = 'walk'
        self.facing_right = True
        self.target = None
        self.attack_range = 30

    def move(self):

        if self.dead:
            self.animate()
            return

        if self.target:

            distance_x = self.rect.centerx - self.target.rect.centerx
            distance_y = self.rect.centery - self.target.rect.centery

        if self.target.rect.centerx > self.rect.centerx:
            self.facing_right = False
        else:
            self.facing_right = True

            # Movimento horizontal
            if abs(distance_x) > self.attack_range:
                self.rect.centerx -= ENTITY_SPEED[self.name]

            # Movimento vertical
            if abs(distance_y) > 20:

                if distance_y > 0:
                    self.rect.centery -= ENTITY_SPEED[self.name]

                else:
                    self.rect.centery += ENTITY_SPEED[self.name]

            if abs(distance_x) > self.attack_range or abs(distance_y) > 20:
                self.state = 'walk'
            else:
                self.state = 'idle'

        self.animate()
