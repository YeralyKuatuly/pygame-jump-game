import pygame
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.player_jump = None
        self.player_walk = None

        # Load images
        self.load_images()

        self.player_index = 0
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(120, Bottom))
        self.rect.width -= 50
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound(Jump_sound)
        self.jump_sound.set_volume(0.5)

    def load_images(self):
        player_walk_1 = pygame.image.load(Player_walk_1).convert_alpha()
        player_walk_2 = pygame.image.load(Player_walk_2).convert_alpha()
        self.player_walk = [
            pygame.transform.scale(player_walk_1, (90, 118)),
            pygame.transform.scale(player_walk_2, (90, 118))
        ]
        self.player_jump = pygame.transform.scale(pygame.image.load(Player_jump).convert_alpha(), (90, 118))

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.bottom >= Bottom:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= Bottom:
            self.rect.bottom = Bottom

    def update_animation(self):
        if self.rect.bottom < Bottom:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.handle_input()
        self.apply_gravity()
        self.update_animation()

    def reset_player(self):
        self.gravity = 0
        self.rect.bottom = Bottom

    def draw(self, screen):
        screen.blit(self.image, self.rect)
