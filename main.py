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

# Initialize Pygame mixer
pygame.mixer.init()

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

# Power Box
powerbox_sprite = pygame.image.load("assets/power_box.png")
shield_sprite = pygame.image.load("assets/shield.png")
scale = 1.2
shield_sprite = pygame.transform.scale(shield_sprite, (int(shield_sprite.get_width() * scale), int(shield_sprite.get_height() * scale)))

background_layers = [pygame.transform.scale(layer, (1920, 1080)) for layer in background_layers]
background_menu = pygame.transform.scale(background_menu, (1920, 1080))
background_pause = pygame.transform.scale(background_pause, (1920, 1080))

# Load sounds
jetpack_sound = pygame.mixer.Sound("assets/jetpack_sound.wav")
death_sound = pygame.mixer.Sound("assets/death_sound.wav")

# Player sprite sheet frames management
SPRITE_WIDTH = 135
SPRITE_HEIGHT = 133
NUM_FRAMES = 4

# Box sprite sheet frames management
BOX_SPRITE_WIDTH = 170
BOX_SPRITE_HEIGHT = 170
NUM_BOX_FRAMES = 7

def get_frame(sheet, frame, y_offset):
    rect = pygame.Rect(frame * SPRITE_WIDTH, y_offset, SPRITE_WIDTH, SPRITE_HEIGHT)
    image = pygame.Surface(rect.size, pygame.SRCALPHA)
    image.blit(sheet, (0, 0), rect)
    return image

def get_frame_box(sheet, frame, y_offset):
    rect = pygame.Rect(frame * BOX_SPRITE_WIDTH, y_offset, BOX_SPRITE_WIDTH, BOX_SPRITE_HEIGHT)
    image = pygame.Surface(rect.size, pygame.SRCALPHA)
    image.blit(sheet, (0, 0), rect)
    return image

# Box management
frames_box = [get_frame_box(powerbox_sprite, i, 0) for i in range(NUM_BOX_FRAMES)]
box_rect = pygame.Rect(400, 1020, BOX_SPRITE_WIDTH, BOX_SPRITE_HEIGHT)
box_velocity = [0]
current_box_frame = [0]
frame_box_count = [0]

# Player management
frames_ground = [get_frame(player_sprite, i, 0) for i in range(NUM_FRAMES)]
frames_air = [get_frame(player_sprite, i, SPRITE_HEIGHT) for i in range(NUM_FRAMES)]
player_rect = pygame.Rect(400, 1020, SPRITE_WIDTH, SPRITE_HEIGHT)
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

# Power box management
powerboxes = []
powerbox_timer = [0]
POWERBOX_INTERVAL = [5000]

# Initial laser speed
laser_speed = [5]

# Power-up management
invincibility_duration = [0]
slow_time_duration = [0]
is_invincible = [False]
is_slow_time = [False]

# Score management
score = [0]

# Load best score from file
def load_best_score():
    try:
        with open("best_score.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        print("No best score found, cassé le jeu")
        sys.exit()

# Save best score to file
def save_best_score(score):
    with open("best_score.txt", "w") as file:
        file.write(str(score))

best_score = [load_best_score()]
font = pygame.font.Font("assets/font.ttf", 40)

def create_laser():
    x_pos = random.randint(1920, 3840)
    y_pos = random.randint(180, 900)
    scale = 0.8
    angle = random.randint(0, 360)

    laser = pygame.transform.scale(laser_sprite, (int(laser_sprite.get_width() * scale), int(laser_sprite.get_height() * scale)))
    laser = pygame.transform.rotate(laser, angle)
    laser_rect = laser.get_rect(center=(x_pos, y_pos))

    laser_mask = pygame.mask.from_surface(laser)

    return (laser, laser_rect, laser_mask)

def create_powerbox():
    x_pos = random.randint(1920, 3840)
    y_pos = random.randint(180, 900)
    frame = random.randint(0, NUM_BOX_FRAMES - 1)
    powerbox_image = frames_box[frame]
    powerbox_rect = powerbox_image.get_rect(center=(x_pos, y_pos))

    powerbox_mask = pygame.mask.from_surface(powerbox_image)

    return (powerbox_image, powerbox_rect, powerbox_mask)

def reset_game():
    global player_rect, player_velocity, score, lasers, powerboxes, layer_speeds, laser_speed, invincibility_duration, slow_time_duration, is_invincible, is_slow_time
    player_rect.topleft = (500, 1020)
    player_velocity[0] = 0
    score[0] = 0
    lasers = []
    powerboxes = []
    layer_speeds = [4, 5, 6]
    laser_speed[0] = 5
    LASER_INTERVAL[0] = 2000
    POWERBOX_INTERVAL[0] = 10000
    boost[0] = -10
    gravity[0] = 0.5
    invincibility_duration[0] = 0
    slow_time_duration[0] = 0
    is_invincible[0] = False
    is_slow_time[0] = False

def display(player_rect, frames_ground, frames_air, background_layers, layer_positions, lasers, powerboxes, score):
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

    for powerbox in powerboxes:
        screen.blit(powerbox[0], powerbox[1].topleft)

    score_text = font.render("Score: " + str(score[0]), True, (255, 255, 255))
    best_score_text = font.render("Best Score: " + str(best_score[0]), True, (255, 255, 255))

    screen.blit(score_text, (50, 50))
    screen.blit(best_score_text, (50, 100))

    pygame.display.flip()

def menu():
    menu_open = True
    while menu_open:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_best_score(best_score[0])
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    menu_open = False

        screen.blit(background_menu, (0, 0))
        pygame.display.flip()

def pause():
    pause_open = True
    while pause_open:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_best_score(best_score[0])
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_open = False

        screen.blit(background_pause, (0, 0))
        pygame.display.flip()

def handle_powerbox(player_rect, powerboxes, is_invincible, is_slow_time, invincibility_duration, slow_time_duration):
    player_mask = pygame.mask.from_surface(frames_ground[current_frame[0]])

    for powerbox in powerboxes[:]:
        if player_mask.overlap(powerbox[2], (powerbox[1].x - player_rect.x, powerbox[1].y - player_rect.y)):
            effect = random.choice(["invincibility", "slow_time"])
            if effect == "invincibility":
                is_invincible[0] = True
                invincibility_duration[0] = pygame.time.get_ticks() + 5000
            elif effect == "slow_time":
                is_slow_time[0] = True
                slow_time_duration[0] = pygame.time.get_ticks() + 5000
            powerboxes.remove(powerbox)

def update_powerups(is_invincible, is_slow_time, invincibility_duration, slow_time_duration, laser_speed, layer_speeds):
    current_time = pygame.time.get_ticks()

    if is_invincible[0] and current_time > invincibility_duration[0]:
        is_invincible[0] = False

    if is_slow_time[0] and current_time > slow_time_duration[0]:
        is_slow_time[0] = False
        laser_speed[0] = 5
        layer_speeds[:] = [4, 5, 6]

def laser_manage(player_rect, lasers, is_invincible):
    player_mask = pygame.mask.from_surface(frames_ground[current_frame[0]])

    for laser in lasers:
        laser[1].x -= laser_speed[0]
        offset = (laser[1].x - player_rect.x, laser[1].y - player_rect.y)

        if not is_invincible[0] and player_mask.overlap(laser[2], offset):
            death_sound.play()
            return True

    return False

def main():
    menu()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_best_score(best_score[0])
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_SPACE]:
            if not pygame.mixer.get_busy():
                jetpack_sound.play()
            player_velocity[0] = boost[0]
        else:
            jetpack_sound.stop()

        player_velocity[0] += gravity[0]
        player_rect.y += player_velocity[0]

        for i in range(len(layer_speeds)):
            layer_positions[i] -= layer_speeds[i]
            if layer_positions[i] <= -1920:
                layer_positions[i] = 0

        if player_rect.bottom >= 1020:
            player_rect.bottom = 1020
            player_velocity[0] = 0

        frame_count[0] += 1
        if frame_count[0] >= 5:
            current_frame[0] = (current_frame[0] + 1) % NUM_FRAMES
            frame_count[0] = 0

        laser_timer[0] += clock.get_time()
        if laser_timer[0] >= LASER_INTERVAL[0]:
            lasers.append(create_laser())
            laser_timer[0] = 0

        powerbox_timer[0] += clock.get_time()
        if powerbox_timer[0] >= POWERBOX_INTERVAL[0]:
            powerboxes.append(create_powerbox())
            powerbox_timer[0] = 0

        powerbox_timer[0] += clock.get_time()
        if powerbox_timer[0] >= 5000:
            current_box_frame[0] = (current_box_frame[0] + 1) % NUM_BOX_FRAMES
            powerbox_timer[0] = 0

        handle_powerbox(player_rect, powerboxes, is_invincible, is_slow_time, invincibility_duration, slow_time_duration)
        update_powerups(is_invincible, is_slow_time, invincibility_duration, slow_time_duration, laser_speed, layer_speeds)

        for laser in lasers[:]:
            if laser[1].right < 0:
                lasers.remove(laser)

        for powerbox in powerboxes[:]:
            if powerbox[1].right < 0:
                powerboxes.remove(powerbox)

        score[0] += 1
        if score[0] > best_score[0]:
            best_score[0] = score[0]

        if laser_manage(player_rect, lasers, is_invincible):
            save_best_score(best_score[0])
            reset_game()
            menu()

        display(player_rect, frames_ground, frames_air, background_layers, layer_positions, lasers, powerboxes, score)
        clock.tick(FPS)

if __name__ == "__main__":
    main()
