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

# Initialize Pygame mixer
pygame.mixer.init()

# Load sounds
jetpack_sound = pygame.mixer.Sound("assets/jetpack_sound.wav")
death_sound = pygame.mixer.Sound("assets/death_sound.wav")

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
POWERBOX_INTERVAL = [20000]

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
    if is_invincible[0]:
        screen.blit(shield_sprite, (player_rect.x - 10, player_rect.y - 10))

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
    # handle frame
    for i in range(len(background_layers)):
        layer_positions[i] -= layer_speeds[i]
        if layer_positions[i] <= -1920:
            layer_positions[i] = 0

    laser_timer[0] += clock.get_time()
    if laser_timer[0] >= LASER_INTERVAL[0]:
        lasers.append(create_laser())
        laser_timer[0] = 0

    for laser in lasers[:]:
        laser[1].x -= laser_speed[0]
        if laser[1].right < 0:
            lasers.remove(laser)
    player_mask = pygame.mask.from_surface(frames_ground[current_frame[0]] if player_velocity[0] >= 0 and player_rect.bottom >= 1020 else frames_air[current_frame[0]])
    for laser in lasers:
        offset = (laser[1].x - player_rect.x, laser[1].y - player_rect.y)
        if not is_invincible[0] and player_mask.overlap(laser[2], offset):
            death_sound.play()
            return True
    return False

def powerbox_manage():
    powerbox_timer[0] += clock.get_time()
    if powerbox_timer[0] >= POWERBOX_INTERVAL[0]:
        powerboxes.append(create_powerbox())
        powerbox_timer[0] = 0

    for powerbox in powerboxes[:]:
        powerbox[1].x -= 4
        if powerbox[1].right < 0:
            powerboxes.remove(powerbox)

    player_mask = pygame.mask.from_surface(frames_ground[current_frame[0]] if player_velocity[0] >= 0 and player_rect.bottom >= 1020 else frames_air[current_frame[0]])
    for powerbox in powerboxes:
        offset = (powerbox[1].x - player_rect.x, powerbox[1].y - player_rect.y)
        if player_mask.overlap(powerbox[2], offset):
            powerboxes.remove(powerbox)
            activate_powerup()

def activate_powerup():
    powerup_type = random.choice(["invincibility", "slow_time"])
    if powerup_type == "invincibility":
        invincibility_duration[0] = 3000
        is_invincible[0] = True
    elif powerup_type == "slow_time":
        slow_time_duration[0] = 5000
        is_slow_time[0] = True
        global FPS
        FPS = 30

def update_powerups():
    if invincibility_duration[0] > 0:
        invincibility_duration[0] -= clock.get_time()
        if invincibility_duration[0] <= 0:
            is_invincible[0] = False

    if slow_time_duration[0] > 0:
        slow_time_duration[0] -= clock.get_time()
        if slow_time_duration[0] <= 0:
            is_slow_time[0] = False
            global FPS
            FPS = 60  # Restore normal game speed

def display_menu():
    running = True
    start_button = Button("Start", 860, 500, 200, 100, (100, 255, 100), (50, 205, 50), "start")
    quit_button = Button("Quit", 860, 650, 200, 100, (165, 10, 45), (155, 0, 35), "quit")
    while running:
        screen.fill((0, 0, 0))
        screen.blit(background_menu, (0, 0))
        start_button.draw(screen)
        quit_button.draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
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

    for powerbox in powerboxes:
        screen.blit(powerbox[0], powerbox[1].topleft)

    score_text = font.render(f'Score: {score[0]}', True, (255, 255, 255))
    screen.blit(score_text, (1600, 50))
    score_text = font.render("PAUSE", True, (255, 255, 255))
    screen.blit(score_text, (960, 500))
    score_resume = font.render("Press any key to resume", True, (255, 255, 255))
    screen.blit(score_resume, (800, 600))
    screen.blit(background_pause, (0, 0))

    pygame.display.flip()
    clock.tick(FPS)

def display_end():
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

    score_text = font.render(f'SCORE: {score[0]}', True, (255, 9, 255))
    screen.blit(score_text, (1600, 50))
    score_text = font.render("GAME OVER", True, (200, 200, 200))
    screen.blit(score_text, (960, 500))
    score_resume = font.render("Press any key to restart", True, (200, 200, 200))
    screen.blit(score_resume, (800, 600))
    score_resume = font.render("Press ESC to go back to menu", True, (200, 200, 200))
    screen.blit(score_resume, (800, 650))
    score_best = font.render(f"Best score: {best_score[0]}", True, (9, 200, 200))
    screen.blit(score_best, (800, 700))
    screen.blit(background_pause, (0, 0))

    pygame.display.flip()
    clock.tick(FPS)

def game_loop():
    running = 1
    state = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            tmp = 0
            if event.type == pygame.KEYDOWN and state == 1:
                state = 0
                tmp = 1
            if state != 2 and event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and tmp == 0:
                state = not state
            if state == 2 and event.type == pygame.KEYDOWN:
                reset_game()
                if (event.key == pygame.K_ESCAPE):
                    return 0
                state = 0
            
        # Player management
        keys = pygame.key.get_pressed()
        
        if state == 1:
            display_pause()
            continue
        if state == 2:
            display_end()
            continue
        if keys[pygame.K_UP] or keys[pygame.K_SPACE]:
            if not pygame.mixer.get_busy():
                jetpack_sound.play()
            player_velocity[0] = boost[0]
        else:
            jetpack_sound.stop()
        
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
        
        score[0] += 1
        if laser_manage():
            best_score[0] = load_best_score()
            if score[0] > best_score[0]:
                best_score[0] = score[0]
                save_best_score(best_score[0])
            state = 2

        # Manage powerboxes
        powerbox_manage()

        # Update power-up effects
        update_powerups()

        if score[0] % 150 == 0:
            for i in range(len(layer_speeds)):
                layer_speeds[i] += 0.5
            laser_speed[0] += 0.5
            LASER_INTERVAL[0] -= 40
            gravity[0] += 0.01
            boost[0] -= 0.015

        # Display the game
        display(player_rect, frames_ground, frames_air, background_layers, layer_positions, lasers, powerboxes, score)
    return running

def main():
    running = 1
    state = 0
    while running:
        if state == 0:
            state = display_menu()
        if state == 1:
            state = game_loop()
        if state == -1:
            running = 0
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
