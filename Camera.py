import pygame

from models.Characters import Player


class CameraGroup(pygame.sprite.Group):
    def __init__(self, surf):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        self.ground_surf = surf
        self.ground_rect = self.ground_surf.get_rect(topleft=(0, 0))

    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def draw_camera(self, player: Player):
        self.center_target_camera(player)
        ground_offset = self.ground_rect.topleft - self.offset
        self.display_surface.blit(self.ground_surf, ground_offset)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

        # draw game UI
        font = pygame.font.Font(None, 20)
        background_ui = pygame.Surface((800, 50))
        health_stats = font.render(f"Health: {player.health}/100", False, "White")
        mana_stats = font.render(f"Mana: {player.mana}/100", False, "White")
        coin_stats = font.render(f"Coins: {player.score}", False, "White")
        background_ui.fill((0, 0, 0))
        background_ui.blit(health_stats, (50, 15))
        background_ui.blit(mana_stats, (50, 30))
        background_ui.blit(coin_stats, (700, 22))
        self.display_surface.blit(background_ui, (0, 550))
