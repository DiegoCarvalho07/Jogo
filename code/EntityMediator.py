from code.Const import ENEMY_ATTACK_RANGE_X, ENEMY_ATTACK_RANGE_Y, WIN_WIDTH
from code.Enemy import Enemy
from code.Entity import Entity
from code.Player import Player


class EntityMediator:

    @staticmethod
    def __verify_collision_window(ent: Entity):

        if isinstance(ent, Enemy):
            if ent.rect.right <= 0:
                ent.health = 0

    @staticmethod
    def __verify_collision_entity(ent1, ent2):

        if ent1.dead or ent2.dead:
            return

        if isinstance(ent1, Player) and isinstance(ent2, Enemy):

            if (
                ent1.rect.right >= ent2.rect.left and
                ent1.rect.left <= ent2.rect.right and
                ent1.rect.bottom >= ent2.rect.top and
                ent1.rect.top <= ent2.rect.bottom
            ):

                # ATAQUE DO JOGADOR
                if (
                    ent1.attacking
                    and ent1.frame < 1
                    and not ent1.hit_registered
                ):

                    attack_rect = ent1.get_attack_rect()

                    if attack_rect.colliderect(ent2.rect):

                        distance_y = abs(
                            ent1.rect.centery -
                            ent2.rect.centery
                        )

                        if distance_y < 25:

                            ent2.take_damage(ent1.damage)

                            knockback_enemy = 15

                            if ent2.rect.centerx > ent1.rect.centerx:
                                ent2.rect.x += knockback_enemy
                            else:
                                ent2.rect.x -= knockback_enemy

                            ent2.attacking = False
                            ent2.hit_registered = True
                            ent2.frame = 0
                            ent2.last_dmg = ent1.name

                            ent1.hit_registered = True
                            ent1.attack_cooldown = 10
                # ATAQUE DO INIMIGO
                if (
                    ent2.attacking
                    and not ent2.hit_registered
                    and ent2.frame >= 1
                ):
                    if ent1.hurt:
                        return

                    distance_x = abs(
                        ent1.rect.centerx -
                        ent2.rect.centerx
                    )

                    distance_y = abs(
                        ent1.rect.centery -
                        ent2.rect.centery
                    )

                    if distance_x < ENEMY_ATTACK_RANGE_X and distance_y < ENEMY_ATTACK_RANGE_Y:

                        if ent1.hurt:
                            return

                        if ent1.invincible_timer > 0:
                            return

                        ent1.take_damage(ent2.damage)
                        ent1.attack_lock_timer = 30
                        ent1.attacking = False

                        if ent1.rect.centerx < ent2.rect.centerx:
                            ent1.rect.x -= 10
                        else:
                            ent1.rect.x += 10

                        if ent1.rect.left < 50:
                            ent1.rect.left = 50

                        if ent1.rect.right > WIN_WIDTH - 40:
                            ent1.rect.right = WIN_WIDTH - 40

                        knockback_enemy = 15

                        if ent2.rect.centerx > ent1.rect.centerx:
                            ent2.rect.x += knockback_enemy
                        else:
                            ent2.rect.x -= knockback_enemy

                        if ent2.rect.left < 50:
                            ent2.rect.left = 50

                        if ent2.rect.right > WIN_WIDTH - 40:
                            ent2.rect.right = WIN_WIDTH - 40

                        ent1.last_dmg = ent2.name
                        ent2.hit_registered = True
                        ent2.attack_cooldown = 120

    @staticmethod
    def __give_score(enemy: Enemy, entity_list: list[Entity]):
        
        for ent in entity_list:

            if isinstance(ent, Player):

                ent.score += enemy.score

                break

    @staticmethod
    def verify_collision(entity_list: list[Entity]):

        for i in range(len(entity_list)):

            entity1 = entity_list[i]

            EntityMediator.__verify_collision_window(
                entity1
            )

            for j in range(i + 1, len(entity_list)):

                entity2 = entity_list[j]

                EntityMediator.__verify_collision_entity(
                    entity1,
                    entity2
                )

    @staticmethod
    def verify_health(entity_list: list[Entity]):

        enemies_removed = 0

        for ent in entity_list[:]:

            if ent.dead:

                if ent.death_timer > 0:
                    ent.death_timer -= 1

                else:

                    if isinstance(ent, Enemy):
                        EntityMediator.__give_score(
                            ent,
                            entity_list
                        )

                        entity_list.remove(ent)

                        enemies_removed += 1

        return enemies_removed