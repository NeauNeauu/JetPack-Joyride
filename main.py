#!/usr/bin/python3
## EPITECH PROJECT, 2023
## jetpack_joyride
## File description:
## main.py
##

import pygame
import sys
import random

# Initialize Pygame
pygame.init()

screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Jetpack Joyride")

player_sprite = pygame.image.load("assets/player.png")

# Background layers
background_layers = [
    pygame.image.load("assets/background.jpg"),
    pygame.image.load("assets/background.jpg"),
    pygame.image.load("assets/background.jpg")
]
laser_sprite = pygame.image.load("assets/laser.png")
background_menu = pygame.image.load("assets/background_menu.png")
background_pause = pygame.image.load("assets/background_pause.png")

background_layers = [pygame.transform.scale(layer, (1920, 1080)) for layer in background_layers]
background_menu = pygame.transform.scale(background_menu, (1920, 1080))
background_pause = pygame.transform.scale(background_pause, (1920, 1080))


# Player sprite sheet frames management
SPRITE_WIDTH = 135
SPRITE_HEIGHT = 133
NUM_FRAMES = 4

def get_frame(sheet, frame, y_offset):
    rect = pygame.Rect(frame * SPRITE_WIDTH, y_offset, SPRITE_WIDTH, SPRITE_HEIGHT)
    image = pygame.Surface(rect.size, pygame.SRCALPHA)
    image.blit(sheet, (0, 0), rect)
    return image

frames_ground = [get_frame(player_sprite, i, 0) for i in range(NUM_FRAMES)]
frames_air = [get_frame(player_sprite, i, SPRITE_HEIGHT) for i in range(NUM_FRAMES)]

player_rect = pygame.Rect(500, 1020, SPRITE_WIDTH, SPRITE_HEIGHT)
gravity = [0.5]
boost = [-10]
player_velocity = [0]
current_frame = [0]
frame_count = [0]


# Initial background layer speeds
layer_speeds = [4, 5, 6]
layer_positions = [0, 0, 0]

clock = pygame.time.Clock()
FPS = 60

lasers = []
laser_timer = [0]
LASER_INTERVAL = [2000]

# Initial laser speed
laser_speed = [5]

score = [0]
font = pygame.font.Font("assets/font.ttf", 40)


def create_laser():
    x_pos = random.randint(1920, 3840)
    y_pos = random.randint(180, 900)
    scale = 0.8
    angle = random.randint(0, 360)

    laser = pygame.transform.scale(laser_sprite, (int(laser_sprite.get_width() * scale), int(laser_sprite.get_height() * scale)))
    laser = pygame.transform.rotate(laser, angle)
    laser_rect = laser.get_rect(center=(x_pos, y_pos))

    # Create mask for laser
    laser_mask = pygame.mask.from_surface(laser)

    return (laser, laser_rect, laser_mask)


def reset_game():
    global player_rect, player_velocity, score, lasers, layer_speeds, laser_speed
    player_rect.topleft = (500, 1020)
    player_velocity[0] = 0
    score[0] = 0
    lasers = []
    layer_speeds = [4, 5, 6]
    laser_speed[0] = 5
    LASER_INTERVAL[0] = 2000


def display(player_rect, frames_ground, frames_air, background_layers, layer_positions, lasers, score):
    screen.fill((0, 0, 0))

    for i in range(len(background_layers)):
        screen.blit(background_layers[i], (layer_positions[i], 0))
        screen.blit(background_layers[i], (layer_positions[i] + 1920, 0))
    
    if player_velocity[0] < 0 or player_rect.bottom < 1020:
        screen.blit(frames_air[current_frame[0]], player_rect.topleft)
    else:
        screen.blit(frames_ground[current_frame[0]], player_rect.topleft)

    for laser in lasers:
        screen.blit(laser[0], laser[1].topleft)

    score_text = font.render(f'Score: {score[0]}', True, (255, 255, 255))
    screen.blit(score_text, (1600, 50))

    pygame.display.flip()
    clock.tick(FPS)


class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, action):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.hover_color = hover_color
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        mouse_pos = pygame.mouse.get_pos()
        if self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[1] < self.y + self.height:
            pygame.draw.rect(screen, self.hover_color, (self.x, self.y, self.width, self.height))
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))
        screen.blit(text_surface, text_rect)


def laser_manage():
    for i in range(len(background_layers)):
        layer_positions[i] -= layer_speeds[i]
        if layer_positions[i] <= -1920:
            layer_positions[i] = 0

    laser_timer[0] += clock.get_time()
    if laser_timer[0] >= LASER_INTERVAL[0]:
        lasers.append(create_laser())
        laser_timer[0] = 0

    for laser in lasers[:]:
        laser[1].x -= laser_speed[0]  # Use laser speed here
        if laser[1].right < 0:
            lasers.remove(laser)
    player_mask = pygame.mask.from_surface(frames_ground[current_frame[0]] if player_velocity[0] >= 0 and player_rect.bottom >= 1020 else frames_air[current_frame[0]])
    for laser in lasers:
        offset = (laser[1].x - player_rect.x, laser[1].y - player_rect.y)
        if player_mask.overlap(laser[2], offset):
            reset_game()
            return True
    return False


# Function to display menu
def display_menu():
    running = True
    start_button = Button("Start", 860, 500, 200, 100, (0, 0, 255), (0, 0, 200), "start")
    quit_button = Button("Quit", 860, 650, 200, 100, (255, 0, 0), (200, 0, 0), "quit")
    while running:
        screen.fill((0, 0, 0))
        screen.blit(background_menu, (0, 0))
        start_button.draw(screen)
        quit_button.draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button.x < mouse_pos[0] < start_button.x + start_button.width and start_button.y < mouse_pos[1] < start_button.y + start_button.height:
                    running = False
                if quit_button.x < mouse_pos[0] < quit_button.x + quit_button.width and quit_button.y < mouse_pos[1] < quit_button.y + quit_button.height:
                    pygame.quit()
                    sys.exit()
    return 1


def display_pause():
    screen.fill((0, 0, 0))

    for i in range(len(background_layers)):
        screen.blit(background_layers[i], (layer_positions[i], 0))
        screen.blit(background_layers[i], (layer_positions[i] + 1920, 0))
    
    if player_velocity[0] < 0 or player_rect.bottom < 1020:
        screen.blit(frames_air[current_frame[0]], player_rect.topleft)
    else:
        screen.blit(frames_ground[current_frame[0]], player_rect.topleft)

    for laser in lasers:
        screen.blit(laser[0], laser[1].topleft)

    score_text = font.render(f'Score: {score[0]}', True, (255, 255, 255))
    screen.blit(score_text, (1600, 50))
    score_text = font.render("PAUSE", True, (255, 255, 255))
    screen.blit(score_text, (960, 500))
    score_resume = font.render("Press any key to resume", True, (255, 255, 255))
    screen.blit(score_resume, (800, 600))
    screen.blit(background_pause, (0, 0))

    pygame.display.flip()
    clock.tick(FPS)


# Main game loop
def game_loop():
    running = 1
    pause = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            tmp = 0
            if event.type == pygame.KEYDOWN and pause == 1:
                pause = 0
                tmp = 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and tmp == 0:
                pause = not pause
        
        # Player management
        keys = pygame.key.get_pressed()
        
        if pause == 1:
            display_pause()
            continue
        if keys[pygame.K_UP] or keys[pygame.K_SPACE]:
            player_velocity[0] = boost[0]
        
        player_velocity[0] += gravity[0]
        player_rect.y += player_velocity[0]
        
        if player_rect.top < 0:
            player_rect.top = 0
            player_velocity[0] = 0
        if player_rect.bottom > 1020:
            player_rect.bottom = 1020
            player_velocity[0] = 0
        
        frame_count[0] += 1
        if frame_count[0] >= 10:
            current_frame[0] = (current_frame[0] + 1) % NUM_FRAMES
            frame_count[0] = 0
        
        if (laser_manage() == True):
            running = 0
            break

        score[0] += 1

        # Increase background laser player speed every 200 points
        if score[0] % 150 == 0:
            for i in range(len(layer_speeds)):
                layer_speeds[i] += 0.5
            laser_speed[0] += 0.5
            LASER_INTERVAL[0] -= 40
            gravity[0] += 0.0075
            boost[0] -= 0.0075

        # Display the game
        display(player_rect, frames_ground, frames_air, background_layers, layer_positions, lasers, score)
    return running

def main():
    running = 1
    state = 0
    while running:
        if (state == 0):
            state = display_menu()
        if (state == 1):
            state = game_loop()
        if (state == -1):
            running = 0
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()