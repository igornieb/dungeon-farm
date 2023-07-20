from random import randrange, random
import pygame.sprite
from models.Walls import Wall
from models.Characters import *
from perlin_noise import PerlinNoise

# TODO place player, collisions between enemies and walls

class Level:
    def __init__(self, player: Player, size: tuple, enemies_no: int, enemies_damage_range: tuple,
                 enemies_health_range: tuple, enemies_eye_range: tuple):
        self.player = player
        self.size = size
        self.walls = self.create_walls(size)
        self.enemies = self.create_enemies(enemies_no, enemies_damage_range, enemies_health_range)
        self.ground_items = pygame.sprite.Group()
        self.enemies_eye_range = enemies_eye_range
        self.background = pygame.image.load('assets/level1.png')

        # place player in free space
        for i in range(size[0]):
            for j in range(size[1]):
                self.player.rect.center = i, j
                if not collidegroup(self.player, self.walls):
                    break
            else:
                continue  # only executed if the inner loop did NOT break
            break

    def create_walls(self, size: tuple):
        walls = pygame.sprite.Group()
        noise = PerlinNoise(octaves=10, seed=int(random()))
        xpix, ypix = size[1], size[0]
        map = [[noise([i / xpix, j / ypix]) for j in range(0, xpix, 10)] for i in range(0, ypix, 10)]
        for i in range(0, ypix // 10):
            for j in range(0, xpix // 10):
                if map[i][j] > 0.3:
                    walls.add(Wall(position=(i * 10, j * 10)))
        return walls

    def create_enemies(self, enemies_no, enemies_damage_range, enemies_health_range) -> list[Enemy]:
        enemies = pygame.sprite.Group()
        for i in range(enemies_no):
            enemies.add(Enemy(health=randrange(start=enemies_health_range[0], stop=enemies_health_range[1]),
                              damage_range=enemies_damage_range,
                              position=(randint(1, self.size[0] - 1), randint(1, self.size[1] - 1)), range=2))
        return enemies

    def check_damage(self):
        for enemy in self.enemies:
            if distance(self.player.rect.centerx, self.player.rect.centery, enemy.rect.centerx,
                        enemy.rect.centery) < enemy.attack_range:
                enemy.fighting()
                self.player.get_damage(enemy.get_hit())
            enemy.set_texture()

    def check_items(self):
        items = pygame.sprite.spritecollide(self.player, self.ground_items, False)
        for item in self.ground_items:
            # grab items if close enough
            if distance(self.player.rect.centerx, self.player.rect.centery, item.rect.centerx,
                        item.rect.centery) < self.player.rect.height * 2:
                self.player.score += item.amount
                item.kill()

    def move_enemies(self, offset):
        for enemy in self.enemies:
            enemy.move(self.player, self.enemies_eye_range, offset, self.walls)

    def update(self, offset: tuple):
        self.enemies.update()
        self.check_items()
        self.check_damage()
        self.move_enemies(offset)
        self.player.update_state(self.walls)
