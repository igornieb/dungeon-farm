import math
import pygame


def collidegroup(sprite: pygame.sprite.Sprite, sprite_group: pygame.sprite.Group) -> bool:
    for s in sprite_group:
        if distance(sprite.rect.centerx, sprite.rect.centery, s.rect.centerx, s.rect.centery) < ((sprite.rect.height + sprite.rect.width)/2 * math.sqrt(2)):
            return True
    return False


def distance(x1: int, y1: int, x2: int, y2: int) -> float:
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
