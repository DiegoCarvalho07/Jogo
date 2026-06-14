from code.Const import PLAYER_ATTACK_RANGE_X, PLAYER_ATTACK_RANGE_Y
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

                        if distance_y < 5:

                            print("Vida antes:", ent2.health)

                            ent2.health -= ent1.damage
                            ent2.last_dmg = ent1.name

                            print("Vida depois:", ent2.health)

                            ent1.hit_registered = True
                            ent1.attack_cooldown = 60
                # ATAQUE DO INIMIGO
                if (
                    ent2.attacking
                    and not ent2.hit_registered
                    and ent2.frame >= 1
                ):

                    distance_x = abs(
                        ent1.rect.centerx -
                        ent2.rect.centerx
                    )

                    distance_y = abs(
                        ent1.rect.centery -
                        ent2.rect.centery
                    )

                    if distance_x < PLAYER_ATTACK_RANGE_X and distance_y < PLAYER_ATTACK_RANGE_Y:

                        ent1.health -= 10
                        ent1.last_dmg = ent2.name

                        ent2.hit_registered = True

                        print(
                            f"{ent2.name} acertou!"
                        )

                        print(
                            f"Vida jogador: {ent1.health}"
                        )

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

        for ent in entity_list[:]:

            if ent.health <= 0 and not ent.dead:

                print(f"{ent.name} MORREU")

                ent.dead = True
                ent.state = 'death'
                ent.frame = 0

                if isinstance(ent, Enemy):
                    EntityMediator.__give_score(
                        ent,
                        entity_list
                    )

            elif ent.dead:

                death_frames = ent.animations['death']

                if int(ent.frame) >= len(death_frames) - 1:

                    entity_list.remove(ent)