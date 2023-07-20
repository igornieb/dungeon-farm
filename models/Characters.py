import pygame
from random import randint
from pygame import Rect
from models.Items import Coin
from models.Spells import *
from utilis import distance, collidegroup
import math

# todo
RES = W, H = 800, 600


class Character(pygame.sprite.Sprite):

    def __init__(self, health=100, mana=100, damage_range=(50, 90), range=2):
        super().__init__()
        self.health = health
        self.max_health = health
        self.mana = mana
        self.range = range
        self.damage_range = damage_range
        self.alive = True
        self.last_hit = pygame.time.get_ticks()
        self.cooldown = 300

        # keeping track of character orientation
        self.orientation = "l"
        # keeping track of character texture type
        self.play_fighting_animation = False
        self.play_standing = True
        # keeping track of texture timing
        self.image_timer = pygame.time.get_ticks()
        self.current_texture = 0

    def get_damage(self, dmg=1):
        if pygame.time.get_ticks() - self.last_hit > self.cooldown:
            self.last_hit = pygame.time.get_ticks()
            self.health -= dmg
        if self.health <= 0:
            self.alive = False
            self.kill()

    def get_hit(self):
        return randint(self.damage_range[0], self.damage_range[1])


class Player(Character):
    def __init__(self, health=100, mana=100, damage_range=(15, 36), range=4, score=0):
        super().__init__(health, mana, damage_range, range)
        # textures for player
        self.image_list_r = [
            pygame.transform.scale(pygame.image.load('assets/player_r_1.png'), (40, 40)),
            pygame.transform.scale(pygame.image.load('assets/player_r_2.png'), (40, 40)),
            pygame.transform.scale(pygame.image.load('assets/player_r_3.png'), (40, 40)),
        ]
        self.image_list_l = [
            pygame.transform.scale(pygame.image.load('assets/player_l_1.png'), (40, 40)),
            pygame.transform.scale(pygame.image.load('assets/player_l_2.png'), (40, 40)),
            pygame.transform.scale(pygame.image.load('assets/player_l_3.png'), (40, 40)),
        ]
        self.image_list_t = [
            pygame.transform.scale(pygame.image.load('assets/player_t_1.png'), (40, 40)),
            pygame.transform.scale(pygame.image.load('assets/player_t_2.png'), (40, 40)),
            pygame.transform.scale(pygame.image.load('assets/player_t_3.png'), (40, 40)),
        ]
        self.image_list_d = [
            pygame.transform.scale(pygame.image.load('assets/player_d_1.png'), (40, 40)),
            pygame.transform.scale(pygame.image.load('assets/player_d_2.png'), (40, 40)),
            pygame.transform.scale(pygame.image.load('assets/player_d_3.png'), (40, 40)),
        ]

        self.image_list_f_r = [
            pygame.transform.scale(pygame.image.load('assets/player_r_f_1.png'), (50, 50)),
            pygame.transform.scale(pygame.image.load('assets/player_r_f_2.png'), (50, 50)),
            pygame.transform.scale(pygame.image.load('assets/player_r_f_3.png'), (50, 50)),
        ]
        self.image_list_f_l = [
            pygame.transform.scale(pygame.image.load('assets/player_l_f_1.png'), (50, 50)),
            pygame.transform.scale(pygame.image.load('assets/player_l_f_2.png'), (50, 50)),
            pygame.transform.scale(pygame.image.load('assets/player_l_f_3.png'), (50, 50)),
        ]
        self.image_list_f_t = [
            pygame.transform.scale(pygame.image.load('assets/player_t_f_1.png'), (50, 50)),
            pygame.transform.scale(pygame.image.load('assets/player_t_f_2.png'), (50, 50)),
            pygame.transform.scale(pygame.image.load('assets/player_t_f_3.png'), (50, 50)),
        ]
        self.image_list_f_d = [
            pygame.transform.scale(pygame.image.load('assets/player_d_f_1.png'), (50, 50)),
            pygame.transform.scale(pygame.image.load('assets/player_d_f_2.png'), (50, 50)),
            pygame.transform.scale(pygame.image.load('assets/player_d_f_3.png'), (50, 50)),
        ]

        self.image = pygame.image.load('assets/player_r_1.png')
        self.rect = self.image.get_rect(midbottom=(800, 200))
        self.score = score

        # attack range
        self.max_left_click_range = self.image.get_width() * range * 1.5
        self.max_right_click_range = self.image.get_width() * range * 2

        # spell
        self.spell = Fireball(int(self.max_right_click_range), 10)

        # healing timer
        self.last_heal = pygame.time.get_ticks()

    def set_walking_animation(self):
        if pygame.time.get_ticks() - self.image_timer > 100:
            self.image_timer = pygame.time.get_ticks()
            if self.orientation == "d":
                self.image = self.image_list_d[self.current_texture]
            if self.orientation == "t":
                self.image = self.image_list_t[self.current_texture]
            if self.orientation == "r":
                self.image = self.image_list_r[self.current_texture]
            if self.orientation == "l":
                self.image = self.image_list_l[self.current_texture]
            self.current_texture += 1
            self.current_texture = self.current_texture % len(self.image_list_d)

    def set_fighting_animation(self):
        if pygame.time.get_ticks() - self.image_timer > 100:
            self.image_timer = pygame.time.get_ticks()
            if self.orientation == "d":
                self.image = self.image_list_f_d[self.current_texture % 3]
            if self.orientation == "t":
                self.image = self.image_list_f_t[self.current_texture % 3]
            if self.orientation == "r":
                self.image = self.image_list_f_r[self.current_texture % 3]
            if self.orientation == "l":
                self.image = self.image_list_f_l[self.current_texture % 3]
            self.current_texture += 1
        if self.current_texture > 2:
            self.current_texture = self.current_texture % 3
            self.play_fighting_animation = False

    def set_texture(self):
        if self.play_fighting_animation:
            self.set_fighting_animation()
        else:
            if self.play_standing:
                self.current_texture = 0
            self.set_walking_animation()

    def player_input(self, walls):
        keys = pygame.key.get_pressed()
        self.play_standing = False
        if keys[pygame.K_d] and self.rect.right < W:
            self.rect.right += 1
            self.orientation = "r"
            if collidegroup(self, walls):
                self.rect.right -= 1
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.right -= 1
            self.orientation = "l"
            if collidegroup(self, walls):
                self.rect.right += 1
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.top -= 1
            self.orientation = "t"
            if collidegroup(self, walls):
                self.rect.top += 1
        if keys[pygame.K_s] and self.rect.bottom < H - 50:
            self.rect.bottom += 1
            self.orientation = "d"
            if collidegroup(self, walls):
                self.rect.bottom -= 1
        if not keys[pygame.K_d] and not keys[pygame.K_a] and not keys[pygame.K_w] and not keys[pygame.K_s]:
            self.play_standing = True

    def player_attack(self, event, enemies, offset):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for enemy in enemies:
                if pygame.mouse.get_pressed()[0] and distance(event.pos[0] + offset[0], event.pos[1] + offset[1],
                                                              self.rect.centerx,
                                                              self.rect.centery) < self.max_left_click_range and enemy.rect.collidepoint(
                    event.pos + offset):
                    loot = enemy.get_damage(self.get_hit())
                    self.play_fighting_animation = True
                    self.current_texture = 0
                    return enemy.health, False, loot
                if pygame.mouse.get_pressed()[2] and self.spell.can_use(self, enemy):
                    loot = enemy.get_damage(self.get_hit())
                    return enemy.health, True, loot

    def heal(self):
        if pygame.time.get_ticks() - self.last_heal > self.cooldown:
            if self.health < 100:
                self.health += 1
                self.last_heal = pygame.time.get_ticks()
            if self.mana < 100:
                self.last_heal = pygame.time.get_ticks()
                self.mana += 1

    def get_spell(self):
        self.spell.rect.centery = self.rect.centery
        self.spell.rect.centerx = self.rect.centerx
        return self.spell

    def update_state(self, walls):
        self.set_texture()
        self.player_input(walls)
        self.heal()
        self.update()


# in the future this class could be inherited and provide base for diffrent enemies types
class Enemy(Character):
    def __init__(self, health=100, mana=100, position: tuple = (0, 0), damage_range: tuple = (1, 20), range: int = 2):
        super().__init__(health, mana, damage_range, range)
        # enemy textures
        self.image_list_r = [
            pygame.transform.scale(pygame.image.load('assets/enemy_r_1.png'), (40, 40)),
            pygame.transform.scale(pygame.image.load('assets/enemy_r_2.png'), (40, 40)),
            pygame.transform.scale(pygame.image.load('assets/enemy_r_3.png'), (40, 40)),
        ]
        self.image_list_l = [
            pygame.transform.scale(pygame.image.load('assets/enemy_l_1.png'), (40, 40)),
            pygame.transform.scale(pygame.image.load('assets/enemy_l_2.png'), (40, 40)),
            pygame.transform.scale(pygame.image.load('assets/enemy_l_3.png'), (40, 40)),
        ]
        self.image_list_t = [
            pygame.transform.scale(pygame.image.load('assets/enemy_t_1.png'), (40, 40)),
            pygame.transform.scale(pygame.image.load('assets/enemy_t_2.png'), (40, 40)),
            pygame.transform.scale(pygame.image.load('assets/enemy_t_3.png'), (40, 40)),
        ]
        self.image_list_d = [
            pygame.transform.scale(pygame.image.load('assets/enemy_d_1.png'), (40, 40)),
            pygame.transform.scale(pygame.image.load('assets/enemy_d_2.png'), (40, 40)),
            pygame.transform.scale(pygame.image.load('assets/enemy_d_3.png'), (40, 40)),
        ]
        self.image_list_f_r = [
            pygame.transform.scale(pygame.image.load('assets/enemy_r_f_1.png'), (60, 60)),
            pygame.transform.scale(pygame.image.load('assets/enemy_r_f_2.png'), (60, 60)),
            pygame.transform.scale(pygame.image.load('assets/enemy_r_f_3.png'), (60, 60)),
        ]
        self.image_list_f_l = [
            pygame.transform.scale(pygame.image.load('assets/enemy_l_f_1.png'), (60, 60)),
            pygame.transform.scale(pygame.image.load('assets/enemy_l_f_2.png'), (60, 60)),
            pygame.transform.scale(pygame.image.load('assets/enemy_l_f_3.png'), (60, 60)),
        ]
        self.image_list_f_t = [
            pygame.transform.scale(pygame.image.load('assets/enemy_t_f_1.png'), (60, 60)),
            pygame.transform.scale(pygame.image.load('assets/enemy_t_f_2.png'), (60, 60)),
            pygame.transform.scale(pygame.image.load('assets/enemy_t_f_3.png'), (60, 60)),
        ]
        self.image_list_f_d = [
            pygame.transform.scale(pygame.image.load('assets/enemy_d_f_1.png'), (60, 60)),
            pygame.transform.scale(pygame.image.load('assets/enemy_d_f_2.png'), (60, 60)),
            pygame.transform.scale(pygame.image.load('assets/enemy_d_f_3.png'), (60, 60)),
        ]

        self.image = self.image_list_r[0]
        self.rect = self.image.get_rect(topleft=position)
        self.attack_range = self.image.get_width() * 2

    def fighting(self):
        self.play_fighting_animation = True

    def set_walking_animation(self):
        if pygame.time.get_ticks() - self.image_timer > 100:
            self.image_timer = pygame.time.get_ticks()
            if self.orientation == "d":
                self.image = self.image_list_d[self.current_texture]
            if self.orientation == "t":
                self.image = self.image_list_t[self.current_texture]
            if self.orientation == "r":
                self.image = self.image_list_r[self.current_texture]
            if self.orientation == "l":
                self.image = self.image_list_l[self.current_texture]
            self.current_texture += 1
            self.current_texture = self.current_texture % len(self.image_list_d)

    def set_fighting_animation(self):
        if pygame.time.get_ticks() - self.image_timer > 150:
            self.image_timer = pygame.time.get_ticks()
            if self.orientation == "d":
                self.image = self.image_list_f_d[self.current_texture % 3]
            if self.orientation == "t":
                self.image = self.image_list_f_t[self.current_texture % 3]
            if self.orientation == "r":
                self.image = self.image_list_f_r[self.current_texture % 3]
            if self.orientation == "l":
                self.image = self.image_list_f_l[self.current_texture % 3]
            self.current_texture += 1
        if self.current_texture > 2:
            self.current_texture = self.current_texture % 3
            self.play_fighting_animation = False

    def set_texture(self):
        if self.play_fighting_animation:
            self.set_fighting_animation()
        else:
            if self.play_standing:
                self.current_texture = 0
            self.set_walking_animation()

    def get_damage(self, dmg=1):
        if pygame.time.get_ticks() - self.last_hit > self.cooldown:
            self.last_hit = pygame.time.get_ticks()
            self.health -= dmg
        if self.health <= 0:
            self.alive = False
            self.kill()
            return Coin((self.rect.centerx, self.rect.centery), randint(1, 20))

    def move(self, player: Player, enemies_eye_range: tuple, offset: tuple, walls: pygame.sprite.Group):
        if distance(player.rect.centerx + offset[0], player.rect.centery + offset[1], self.rect.centerx,
                    self.rect.centery) < randint(enemies_eye_range[0], enemies_eye_range[1]):
            # move enemies closer to player
            dir_x = player.rect.centerx - self.rect.centerx
            dir_y = player.rect.centery - self.rect.centery
            hyp = math.sqrt(dir_x * dir_x + dir_y * dir_y)
            self.play_standing = False
            if hyp > 0 and not player.rect.colliderect(self):
                dir_x /= hyp
                dir_y /= hyp
                self.rect.centerx += dir_x
                self.rect.centery += dir_y

                if collidegroup(self, walls, offset):
                    self.play_standing = True
                    self.rect.centerx -= dir_x
                    self.rect.centery -= dir_y

            # set direction for textures
            if dir_x >= 0 and dir_x > dir_y:
                self.orientation = "r"
            if 0 >= dir_x > dir_y:
                self.orientation = "l"
            if dir_y >= 0 and dir_x < dir_y:
                self.orientation = "d"
            if 0 >= dir_y > dir_x:
                self.orientation = "t"
        else:
            self.play_standing = True
