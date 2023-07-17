import pygame


class Spell(pygame.sprite.Sprite):
    def __init__(self, name: str, cost: int):
        super().__init__()
        self.name = name
        self.cost = cost

    def use(self, player, character2):
        if player.mana >= self.cost:
            return True
        return False


class Fireball(Spell):
    def in_range(self, center: tuple, enemy: tuple) -> bool:
        if ((enemy[0] - center[0]) ** 2 + (enemy[1] - center[1]) ** 2) <= self.range ** 2:
            return True
        return False

    def __init__(self, range, cost):
        super().__init__('fireball', cost)
        self.range = range + 40
        self.image = pygame.image.load("assets/fireball.png")
        self.image = pygame.transform.scale(self.image, (range + 40, range + 40))
        self.rect = self.image.get_rect()

    def can_use(self, player, character2):
        if self.in_range((character2.rect.centerx, character2.rect.centery),
                         (player.rect.centerx, player.rect.centery)) and player.mana >= self.cost:
            player.mana -= self.cost
            return True
        return False
