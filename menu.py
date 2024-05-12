import pygame
from pygame.locals import QUIT, KEYDOWN, K_RETURN
from settings import *


class Menu:
    def __init__(self):
        pygame.init()

        self.width = Width
        self.height = Height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Game Menu')

        self.clock = pygame.time.Clock()
        self.font_size = 60
        self.font = pygame.font.Font(my_font_path, self.font_size)

        self.menu_options = [
            "Start Game",
            "Top Scores",
            "Reset Top Scores",
            "Exit"
        ]

        self.selected_option = 0
        self.colors = {
            "normal": (255, 255, 255),
            "selected": (255, 0, 0)
        }

        self.running = True
        self.button_sound = pygame.mixer.Sound(menu_button)
        self.button_sound.set_volume(0.5)

    def show_menu(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        self.button_sound.play()
                        return self.selected_option
                if event.type == KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.button_sound.play()
                        self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                    elif event.key == pygame.K_UP:
                        self.button_sound.play()
                        self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                    elif event.key == K_RETURN:
                        self.handle_option()

            background_image = pygame.image.load(menu_background)
            background_image = pygame.transform.scale(background_image, (self.width, self.height))
            self.screen.blit(background_image, (0, 0))
            self.render_menu()
            pygame.display.flip()
            self.clock.tick(FPS)

    def render_menu(self):
        for i, option in enumerate(self.menu_options):
            color = self.colors["selected"] if i == self.selected_option else self.colors["normal"]
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=(self.width // 2, self.height // 2 - 90 + i * self.font_size))
            self.screen.blit(text, text_rect)

    def handle_option(self):
        selected_option = self.menu_options[self.selected_option]

        if selected_option == "Start Game":
            # Start Game
            self.running = False
        elif selected_option == "Exit":
            # Exit
            self.running = False
            pygame.quit()
            exit()
