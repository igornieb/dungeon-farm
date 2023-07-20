import pygame


class Wall(pygame.sprite.Sprite):
    def __init__(self, position: tuple):
        super().__init__()
        self.image = pygame.image.load('assets/wall.png')
        self.rect = self.image.get_rect(topleft=position)
