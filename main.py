import pygame
import sys
import os
import random
from pygame.math import Vector2

screen_width = 860
screen_height = 720
SCREEN = pygame.display.set_mode((screen_width, screen_height))
BACKGROUND_IMAGE = pygame.image.load(os.path.join("Graphics", "Background.png")).convert()
pygame.display.set_caption("Menu")

BG = pygame.image.load("Graphics/Background.png")


def get_font(size):
    return pygame.font.Font("Graphics/font.ttf", size)


class SNAKE:
    def __init__(self):
        self.body = [Vector2(7, 10), Vector2(6, 10), Vector2(5, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False

        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizonal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

        self.bodytr = pygame.image.load('Graphics/body_topright.png').convert_alpha()
        self.bodytl = pygame.image.load('Graphics/body_topleft.png').convert_alpha()
        self.bodybr = pygame.image.load('Graphics/body_bottomright.png').convert_alpha()
        self.bodybl = pygame.image.load('Graphics/body_bottomleft.png').convert_alpha()

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizonal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.bodytl, block_rect)
                    if previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.bodybl, block_rect)
                    if previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.bodytr, block_rect)
                    if previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.bodybr, block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down

    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True


class FRUIT:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class Main:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.fail = False

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.fruit_spawn()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()

        for block in self.snake.body[2:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        game_over_font = pygame.font.Font(None, 75)
        game_over_text = game_over_font.render("Game Over", True, (255, 255, 255))
        game_over_text_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_r:
                        return

            screen.fill((175, 215, 70))
            screen.blit(game_over_text, game_over_text_rect)

            quit_text = game_font.render("Press 'Q' to Quit", True, (56, 74, 12))
            quit_rect = quit_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
            screen.blit(quit_text, quit_rect)

            pygame.display.update()
            clock.tick(60)

    def fruit_spawn(self):
        while self.fruit.pos in self.snake.body:
            self.fruit.randomize()

    def draw_grass(self):
        grass_color = (167, 209, 61)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple_rect = apple.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 10,
                              apple_rect.height)

        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)
        pygame.draw.rect(screen, (58, 76, 14), bg_rect, 2)


def main_menu():
    background = pygame.image.load("Graphics/Background.png").convert()
    background = pygame.transform.scale(background, (cell_number * cell_size, cell_number * cell_size))
    screen.blit(background, (0, 0))
    while True:
        for event_main in pygame.event.get():
            if event_main.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event_main.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event_main.pos):
                    game_loop()
                elif quit_button_rect.collidepoint(event_main.pos):
                    pygame.quit()
                    sys.exit()
                elif credits_button_rect.collidepoint(event_main.pos):
                    show_credits()

        screen.fill((175, 215, 70))
        draw_main_menu()
        pygame.display.update()
        clock.tick(60)


def game_loop():
    main_game = Main()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                main_game.update()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if main_game.snake.direction.y != 1:
                        main_game.snake.direction = Vector2(0, -1)
                if event.key == pygame.K_DOWN:
                    if main_game.snake.direction.y != -1:
                        main_game.snake.direction = Vector2(0, 1)
                if event.key == pygame.K_RIGHT:
                    if main_game.snake.direction.x != -1:
                        main_game.snake.direction = Vector2(1, 0)
                if event.key == pygame.K_LEFT:
                    if main_game.snake.direction.x != 1:
                        main_game.snake.direction = Vector2(-1, 0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    main_game = Main()
                elif quit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                elif credits_button_rect.collidepoint(event.pos):
                    show_credits()

        screen.fill((175, 215, 70))
        main_game.draw_elements()
        pygame.display.update()
        clock.tick(60)


def draw_main_menu():
    title_font = pygame.font.Font(None, 120)
    title_text = title_font.render("SNAKE", True, (56, 74, 12))
    title_rect = title_text.get_rect(center=(cell_number * cell_size // 2, cell_number * cell_size // 2 - 100))
    screen.blit(title_text, title_rect)

    play_button = pygame.Rect(cell_number * cell_size // 2 - 75, cell_number * cell_size // 2, 150, 50)
    pygame.draw.rect(screen, (128, 128, 128), play_button)  # Grey background
    play_text = game_font.render("Play", True, (255, 255, 255))  # White text
    play_text_rect = play_text.get_rect(center=play_button.center)
    screen.blit(play_text, play_text_rect)

    credits_button = pygame.Rect(cell_number * cell_size // 2 - 75, cell_number * cell_size // 2 + 100, 150, 50)
    pygame.draw.rect(screen, (128, 128, 128), credits_button)  # Grey background
    credits_text = game_font.render("Credits", True, (255, 255, 255))  # White text
    credits_text_rect = credits_text.get_rect(center=credits_button.center)
    screen.blit(credits_text, credits_text_rect)

    quit_button = pygame.Rect(cell_number * cell_size // 2 - 75, cell_number * cell_size // 2 + 200, 150, 50)
    pygame.draw.rect(screen, (128, 128, 128), quit_button)  # Grey background
    quit_text = game_font.render("Quit", True, (255, 255, 255))  # White text
    quit_text_rect = quit_text.get_rect(center=quit_button.center)
    screen.blit(quit_text, quit_text_rect)

    global play_button_rect, quit_button_rect, credits_button_rect
    play_button_rect = play_button
    credits_button_rect = credits_button
    quit_button_rect = quit_button

    if play_button_rect.collidepoint(pygame.mouse.get_pos()):
        play_text = game_font.render("Play", True, (255, 255, 255))
    if credits_button_rect.collidepoint(pygame.mouse.get_pos()):
        credits_text = game_font.render("Credits", True, (255, 255, 255))
    if quit_button_rect.collidepoint(pygame.mouse.get_pos()):
        quit_text = game_font.render("Quit", True, (255, 255, 255))


def show_credits():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return

        screen.fill((175, 215, 70))
        credits_text = [
            "This game was created by Team Dragon Byte Z.",
            "Gameplay: Ledion",
            "Menus, UI Functionality and Game Art: Rakel",
            "Tracking and Documentation: Enkel",
            "Additional menus and extra features: Serki and Xhoni",
            "Press any button to go back to the main screen.",
            "Thank you for playing."
        ]

        credits_font = pygame.font.Font(None, 30)
        line_height = credits_font.get_linesize()

        credits_surface = pygame.Surface((cell_number * cell_size, line_height * len(credits_text)))
        credits_surface.fill((0, 0, 0))
        credits_surface.set_alpha(128)

        for i, line in enumerate(credits_text):
            text_surface = credits_font.render(line, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(cell_number * cell_size // 2, line_height * (i + 0.5)))
            credits_surface.blit(text_surface, text_rect)

        screen.blit(credits_surface, ((cell_number * cell_size - credits_surface.get_width()) // 2,
                                      (cell_number * cell_size - credits_surface.get_height()) // 2))

        pygame.display.update()
        clock.tick(60)


pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
apple = pygame.image.load('Graphics/apple.png').convert_alpha()
game_font = pygame.font.Font(None, 50)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 115)

main_game = Main()
main_menu()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_button_rect.collidepoint(event.pos):

                main_game = Main()
            elif quit_button_rect.collidepoint(event.pos):

                pygame.quit()
                sys.exit()
            elif credits_button_rect.collidepoint(event.pos):

                show_credits()

    screen.fill((175, 215, 70))
    draw_main_menu()
    pygame.display.update()
    clock.tick(60)
