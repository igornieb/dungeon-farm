import pygame


class Item(pygame.sprite.Sprite):
    def __init__(self, name: str):
        super().__init__()
        self.name = name


class Coin(Item):
    def __init__(self, location: tuple, amount: int = 1):
        super().__init__(name='coins')
        self.amount = amount
        self.image = pygame.image.load('assets/coin.png')

        self.rect = self.image.get_rect(midbottom=location)
