import pygame.event

from models.Level import *
from Camera import CameraGroup


class Game:
    def __init__(self):
        self.RES = self.W, self.H = 800, 600
        self.FPS = 60
        self.player = Player()
        self.levels = [Level(self.player,
                             (self.W, self.H - 50), 10, (1, 5),
                             (30, 50),
                             (300, 450)), Level(self.player,
                                                (self.W, self.H - 50), 5, (1, 5),
                                                (40, 60), (250, 450))]
        self.play()

    def play(self):
        # level count
        i = 0
        #
        pygame.init()
        pygame.display.set_mode(self.RES)
        pygame.display.set_caption('Game')
        clock = pygame.time.Clock()
        background_ui = pygame.Surface((800, 50))
        font = pygame.font.Font(None, 20)
        screen = pygame.display.set_mode(self.RES)

        level = self.levels[i]

        while True:
            camera = CameraGroup(level.background.convert_alpha())
            camera.player.add(level.player)
            camera.enemies = level.enemies
            camera.static = level.walls

            while level.player.alive:
                screen.fill((0, 0, 0))
                if not level.enemies:
                    break
                camera.static.remove(level.player.get_spell())
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # player attack
                        current_attack = level.player.player_attack(event, level.enemies, camera.offset)

                        if current_attack:
                            if current_attack[0] > 0:
                                attack_label = font.render(f"Enemy X: {current_attack[0]}/100", False, "White")
                            else:
                                attack_label = font.render(f"", False, "White")
                            if current_attack[1]:
                                camera.static.add(level.player.get_spell())
                            if current_attack[2]:
                                level.ground_items.add(current_attack[2])
                            background_area = level.background.convert_alpha()
                            background_area.blit(attack_label, (380, 0))

                # update level, player, enemies
                level.update(camera.offset)
                for gi in level.ground_items:
                    camera.static.add(gi)
                # add ground items
                camera.update()
                camera.draw_camera(level.player)

                pygame.display.update()
                clock.tick(self.FPS)

            # level finished
            screen.fill((0, 0, 0))
            message = font.render("", False, "White")
            if not level.player.alive:
                message = font.render(f"Game over press enter to exit, score: {level.player.score}", False, "White")
            if level.player.alive and self.levels[-1] != level:
                message = font.render(f"You won press enter to begin next level", False, "White")
            if level.player.alive and self.levels[-1] == self.levels[i]:
                message = font.render(f"You won, score: {level.player.score}", False, "White")

            screen.blit(message, (200, 200))

            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            if keys[pygame.K_RETURN]:
                if level.player.alive:
                    if len(self.levels) > i + 1:
                        i += 1
                        level = self.levels[i]
                        level.player.mana = 100
                        level.player.health = 100
                        background_ui.fill((0, 0, 0))
                    else:
                        level.player.alive = False
                else:
                    exit()

            pygame.display.update()
            clock.tick(self.FPS)
