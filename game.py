import sys

import pygame
from random import choice
from player import Player
from obstacles import Obstacle
from menu import Menu
from settings import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Width, Height))
        pygame.display.set_caption('Runner Game')
        self.clock = pygame.time.Clock()
        self.menu = Menu()
        self.player = Player()
        self.score = 0
        self.level = 1
        self.top_scores = [0] * 5
        self.load_top_scores()
        self.paused = False
        self.font = pygame.font.Font(my_font_path, 36)
        self.running = True
        self.start_time = 0
        self.pace_changing = {'speed_add': 2, 'spawn_rate_add': 200}

        self.player = pygame.sprite.GroupSingle()
        self.player.add(Player())

        self.obstacle_group = pygame.sprite.Group()

        self.bg_music = pygame.mixer.Sound(music_path)
        self.bg_music.set_volume(0.37)

        # fly and snail
        self.snail_frames = [pygame.image.load(snail_move_1).convert_alpha(),
                             pygame.image.load(snail_move_2).convert_alpha()]
        self.snail_frame_index = 0
        self.snail_surf = self.snail_frames[self.snail_frame_index]

        self.fly_frames = [pygame.image.load(flight_1).convert_alpha(),
                           pygame.image.load(flight_2).convert_alpha()]
        self.fly_frame_index = 0
        self.fly_surf = self.fly_frames[self.fly_frame_index]

        self.spawn_time = 2000
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, self.spawn_time)

        self.snail_animation_timer = pygame.USEREVENT + 2
        pygame.time.set_timer(self.snail_animation_timer, 100)

        self.fly_animation_timer = pygame.USEREVENT + 3
        pygame.time.set_timer(self.fly_animation_timer, 100)

        self.background_image = pygame.image.load(Sky_image_path1).convert()
        self.ground_image = pygame.image.load(Ground_image_path1).convert()
        self.speed = 4
        self.timer_running = False
        self.start_timer = 0
        self.elapsed_time = 0

    def start_my_timer(self):
        self.timer_running = True
        self.start_time = pygame.time.get_ticks()

    def stop_my_timer(self):
        if self.timer_running:
            self.timer_running = False
            self.elapsed_time += pygame.time.get_ticks() - self.start_time

    def reset_my_timer(self):
        self.timer_running = False
        self.start_time = 0
        self.elapsed_time = 0

    def get_elapsed_time(self):
        if self.timer_running:
            return self.elapsed_time + pygame.time.get_ticks() - self.start_time
        else:
            return self.elapsed_time

    def reset_all(self):
        self.background_image = pygame.image.load(Sky_image_path1).convert()
        self.ground_image = pygame.image.load(Ground_image_path1).convert()
        self.bg_music.stop()
        self.obstacle_group.empty()
        self.level = 1
        self.spawn_time = 2000
        pygame.time.set_timer(self.obstacle_timer, self.spawn_time)
        self.speed = 4
        self.reset_my_timer()
        for p in self.player:
            p.reset_player()

    def collision_sprite(self):  # Check are we lost or not
        # Check for collisions between the player sprite and the obstacle group
        if pygame.sprite.spritecollide(self.player.sprite, self.obstacle_group, False):
            self.check_for_top_score()
            self.reset_all()
            return False
        else:
            return True

    def start_game(self):
        self.screen.fill((0, 0, 0))  # Clear the screen
        pygame.display.update()

        self.bg_music.play(loops=-1)
        self.start_my_timer()

        while self.running:
            self.handle_events()
            if not self.paused:
                self.update_game()
                self.render_game()
                self.running = self.collision_sprite()
                self.display_score_and_level()
            else:
                self.stop_my_timer()
                self.show_pause_screen()
            pygame.display.update()
            self.clock.tick(FPS)

    def handle_events(self):
        chosen_obstacle = ''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    if not self.paused:
                        self.toggle_pause()
                        self.stop_my_timer()
                    else:
                        self.toggle_pause()
                        self.start_my_timer()
            if not self.paused:
                if event.type == self.obstacle_timer:
                    chosen_obstacle = choice(['fly', 'snail', 'snail', 'snail'])
                    self.obstacle_group.add(Obstacle(chosen_obstacle))
                    for obstacles in self.obstacle_group:
                        obstacles.set_speed(self.speed)

                # Animate the Snail
                if event.type == self.snail_animation_timer and chosen_obstacle == 'snail':
                    self.snail_frame_index = 1 - self.snail_frame_index  # Toggle between 0 and 1
                    self.snail_surf = self.snail_frames[self.snail_frame_index]

                # Animate the Fly
                elif event.type == self.fly_animation_timer and chosen_obstacle == 'fly':
                    self.fly_frame_index = 1 - self.fly_frame_index  # Toggle between 0 and 1
                    self.fly_surf = self.fly_frames[self.fly_frame_index]

    def update_game(self):
        self.handle_level_progression()
        self.player.update()
        self.obstacle_group.update()

    def render_game(self):
        self.screen.blit(self.background_image, (0, 0))  # Draw the background image
        self.screen.blit(self.ground_image, (0, Bottom))

        self.player.draw(self.screen)
        self.obstacle_group.draw(self.screen)

    def display_score_and_level(self):
        current_time = self.get_elapsed_time() // 1000  # Convert milliseconds to seconds
        self.score = current_time
        score_text = self.font.render(f'Score: {self.score}', True, (0, 0, 0))
        self.screen.blit(score_text, (15, 10))
        level_text = self.font.render(f'Level: {self.level}', True, (0, 0, 0))
        self.screen.blit(level_text, (15, 40))

    def show_pause_screen(self):
        pause_text = self.font.render('Game Paused - Press P to Resume', True, (0, 0, 0))
        self.screen.blit(pause_text, (Width // 2 - pause_text.get_width() // 2, Height // 2))

    def toggle_pause(self):
        self.paused = not self.paused

    def handle_level_progression(self):
        if self.score != 0 and self.score / self.level == 10:
            self.level_up(self.level + 1)

    def level_up(self, new_level):
        self.level = new_level
        self.increase_obstacle_speed()
        self.show_level_change_notification()
        self.spawn_time -= self.pace_changing['spawn_rate_add']
        pygame.time.set_timer(self.obstacle_timer, self.spawn_time)

    def increase_obstacle_speed(self):
        self.speed += self.pace_changing['speed_add']

    def show_level_change_notification(self):
        self.background_image = pygame.image.load(Sky_image_path2).convert() if self.level % 2 == 0 \
            else pygame.image.load(Sky_image_path1)
        self.ground_image = pygame.image.load(Ground_image_path2).convert() if self.level % 2 == 0 \
            else pygame.image.load(Ground_image_path1)

    def display_top_scores(self):
        # Clear the screen or draw a background
        top_scores_image = pygame.image.load(top_scores_image_path)
        top_scores_image = pygame.transform.scale(top_scores_image, (Width, Height))
        self.screen.blit(top_scores_image, (0, 0))

        # Title for the top scores
        title_font = pygame.font.Font(my_font_path, 80)
        title_text = title_font.render('Top Scores', True, (255, 255, 0))
        self.screen.blit(title_text, (Width // 2 - title_text.get_width() // 2, 150))

        # Display each top score with improved styling
        score_font = pygame.font.Font(my_font_path, 40)
        for i, score in enumerate(self.top_scores):
            score_text = score_font.render(f'{i + 1}. {score}', True, (255, 255, 255))
            score_rect = score_text.get_rect(center=(Width // 2, 250 + i * 60))
            self.screen.blit(score_text, score_rect)

        # Update the display to show the scores
        pygame.display.update()

        # Wait for user input to return to the menu
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    waiting_for_input = False

    def save_top_scores(self):
        with open(records_path, "w") as file:
            for score in self.top_scores:
                file.write(f"{score}\n")

    def reset_top_scores(self):
        self.top_scores = [0] * 5
        self.save_top_scores()

    def load_top_scores(self):
        try:
            with open(records_path, "r") as file:
                self.top_scores = [int(line.strip()) for line in file.readlines()]
        except FileNotFoundError:
            # If the file is not found, initialize with default scores
            self.top_scores = [0] * 5

    def check_for_top_score(self):
        if self.score > min(self.top_scores):
            self.top_scores.append(self.score)
            self.top_scores.sort(reverse=True)
            self.top_scores = self.top_scores[:5]

    def display_menu(self):
        self.reset_all()
        self.running = True

        selected_option = self.menu.show_menu()
        if selected_option == 0:
            pygame.display.update()  # Update display to clear menu graphics
            pygame.time.delay(555)  # Short delay for smooth transition
            self.start_game()
        elif selected_option == 1:
            self.display_top_scores()
        elif selected_option == 2:
            self.reset_top_scores()
        elif selected_option == 3:
            self.save_top_scores()
            pygame.quit()
            exit()
        game.display_menu()


if __name__ == "__main__":
    game = Game()
    game.display_menu()
