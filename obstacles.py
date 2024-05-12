from settings import *
from random import randint
import pygame


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, obstacle_type):
        super().__init__()

        if obstacle_type == 'fly':
            fly_1 = pygame.image.load(flight_1).convert_alpha()
            fly_2 = pygame.image.load(flight_2).convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = Bottom - 120
        else:
            snail_1 = pygame.image.load(snail_move_1).convert_alpha()
            snail_2 = pygame.image.load(snail_move_2).convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = Bottom

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(Width, Width + 350), y_pos))
        self.rect.width -= 50
        self.obstacles_speed = 5

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= self.obstacles_speed
        self.check_and_destroy()

    def check_and_destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def set_speed(self, speed):
        self.obstacles_speed = speed
