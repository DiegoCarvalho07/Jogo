from code.Const import ENTITY_SPEED, ENEMY_ATTACK_RANGE_X, \
    ENEMY_ATTACK_RANGE_Y
from code.Entity import Entity


class Enemy(Entity):

    def __init__(self, name, position):
        super().__init__(name, position)

        self.state = 'walk'
        self.facing_right = True
        self.target = None
        self.attack_range = 30
        self.hit_registered = False
        self.attack_cooldown = 0

    def move(self):

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.dead:
            self.animate()
            return

        if self.target:

            distance_x = abs(
                self.rect.centerx -
                self.target.rect.centerx
            )

            distance_y = abs(
                self.rect.centery -
                self.target.rect.centery
            )
            #print(
            #    self.name,
             #   self.rect.centerx,
              #  self.target.rect.centerx
            #)

            # perto o suficiente para atacar
            if distance_x < ENEMY_ATTACK_RANGE_X and distance_y < ENEMY_ATTACK_RANGE_Y:

                if not self.attacking and self.attack_cooldown == 0:
                    self.hit_registered = False
                    self.frame = 0
                    self.attacking = True
                    self.state = 'attack'

            else:

                self.attacking = False

                # movimento horizontal
                if self.rect.centerx > self.target.rect.centerx:
                    self.rect.centerx -= ENTITY_SPEED[self.name]
                    self.facing_right = True
                else:
                    self.rect.centerx += ENTITY_SPEED[self.name]
                    self.facing_right = False

                # movimento vertical
                if self.rect.centery < self.target.rect.centery:
                    self.rect.centery += ENTITY_SPEED[self.name]
                elif self.rect.centery > self.target.rect.centery:
                    self.rect.centery -= ENTITY_SPEED[self.name]

                self.state = 'walk'
            print(

            self.name,
            "state =", self.state,
            "frame =", int(self.frame),
            "facing =", self.facing_right

            )

        self.animate()