#!/usr/bin/python3
## EPITECH PROJECT, 2023
## jetpack_joyride
## File description:
## main.py
##

import pygame
import sys
import random

pygame.init()

screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Jetpack Joyride")

player_sprite = pygame.image.load("assets/player.png")
background_layers = [
    pygame.image.load("assets/background.jpg"),
    pygame.image.load("assets/background.jpg"),
    pygame.image.load("assets/background.jpg")
]
laser_sprite = pygame.image.load("assets/laser.png")

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
gravity = 0.5
boost = -10
player_velocity = 0
current_frame = 0
frame_count = 0

background_layers = [pygame.transform.scale(layer, (1920, 1080)) for layer in background_layers]

# Initial background layer speeds
layer_speeds = [4, 5, 6]
layer_positions = [0, 0, 0]

clock = pygame.time.Clock()
FPS = 60

lasers = []
laser_timer = 0
LASER_INTERVAL = 2000

# Initial laser speed
laser_speed = 5

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
    player_velocity = 0
    score[0] = 0
    lasers = []
    layer_speeds = [4, 5, 6]
    laser_speed = 5
    LASER_INTERVAL = 2000

def display(player_rect, frames_ground, frames_air, background_layers, layer_positions, lasers, score):
    screen.fill((0, 0, 0))

    for i in range(len(background_layers)):
        screen.blit(background_layers[i], (layer_positions[i], 0))
        screen.blit(background_layers[i], (layer_positions[i] + 1920, 0))
    
    if player_velocity < 0 or player_rect.bottom < 1020:
        screen.blit(frames_air[current_frame], player_rect.topleft)
    else:
        screen.blit(frames_ground[current_frame], player_rect.topleft)

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

# Function to display menu
def display_menu():
    screen.fill((0, 0, 0))
    title_text = font.render("JETPACK JOYRIDE", True, (255, 255, 255))
    screen.blit(title_text, (800, 200))

    play_button.draw(screen)
    exit_button.draw(screen)

    # Initialize buttons
    play_button = Button("Play", 800, 400, 200, 50, (0, 100, 0), (0, 200, 0), "play")
    exit_button = Button("Exit", 800, 500, 200, 50, (100, 0, 0), (200, 0, 0), "exit")

    # Main game loop
    menu_active = True
    while menu_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_button.x < mouse_pos[0] < play_button.x + play_button.width and play_button.y < mouse_pos[1] < play_button.y + play_button.height:
                    menu_active = False
                    # Start game
                elif exit_button.x < mouse_pos[0] < exit_button.x + exit_button.width and exit_button.y < mouse_pos[1] < exit_button.y + exit_button.height:
                    pygame.quit()
                    sys.exit()
    
    display_menu()
    pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Player management
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_UP] or keys[pygame.K_SPACE]:
        player_velocity = boost
    
    player_velocity += gravity
    player_rect.y += player_velocity
    
    if player_rect.top < 0:
        player_rect.top = 0
        player_velocity = 0
    if player_rect.bottom > 1020:
        player_rect.bottom = 1020
        player_velocity = 0
    
    frame_count += 1
    if frame_count >= 10:
        current_frame = (current_frame + 1) % NUM_FRAMES
        frame_count = 0
    
    for i in range(len(background_layers)):
        layer_positions[i] -= layer_speeds[i]
        if layer_positions[i] <= -1920:
            layer_positions[i] = 0

    laser_timer += clock.get_time()
    if laser_timer >= LASER_INTERVAL:
        lasers.append(create_laser())
        laser_timer = 0

    for laser in lasers[:]:
        laser[1].x -= laser_speed  # Use laser speed here
        if laser[1].right < 0:
            lasers.remove(laser)

    player_mask = pygame.mask.from_surface(frames_ground[current_frame] if player_velocity >= 0 and player_rect.bottom >= 1020 else frames_air[current_frame])
    for laser in lasers:
        offset = (laser[1].x - player_rect.x, laser[1].y - player_rect.y)
        if player_mask.overlap(laser[2], offset):
            reset_game()

    score[0] += 1

    # Increase background speed every 200 points
    if score[0] % 300 == 0:
        layer_speeds = [speed + 1 for speed in layer_speeds]
        laser_speed += 1
        LASER_INTERVAL -= 100

    display(player_rect, frames_ground, frames_air, background_layers, layer_positions, lasers, score)

pygame.quit()
sys.exit()
