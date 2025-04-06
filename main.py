import pygame
import sys
from character import Character
from map import Map
import math
import time
import random

# Initialisation
pygame.init()
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Marooned on Mars")

clock = pygame.time.Clock()

# Set initial player and map features
map_size = 10
map_key = {
    'blank': [
        pygame.image.load("assets/tile_1.png").convert_alpha(),
        pygame.image.load("assets/tile_5.png").convert_alpha(),
        pygame.image.load("assets/tile_7.png").convert_alpha(),
        pygame.image.load("assets/tile_8.png").convert_alpha()
    ],
    'mountain': [
        pygame.image.load("assets/tile_2.png").convert_alpha(),
        pygame.image.load("assets/tile_6.png").convert_alpha()
    ],
    'cave': [pygame.image.load("assets/tile_3.png").convert_alpha()],
    'ore': [pygame.image.load("assets/tile_4.png").convert_alpha()]
}

map = Map(map_size, 0, map_key)
map.display_map()

player_x = WIDTH / 2
player_y = HEIGHT / 2
map_x = map_size // 2
map_y = map_size // 2
player_speed = 1
player_hunger = 0
player_thirst = 100
player_fuel = 100
player_oxygen = 100
player_health = 100

player = Character(
    player_x,
    player_y,
    map_x,
    map_y,
    player_speed,
    player_hunger,
    player_thirst,
    player_fuel,
    player_oxygen,
    player_health
)

print(map_x)
print(map_y)

# Display text
health_icon = pygame.image.load("assets/heart.png").convert_alpha()
thirst_icon = pygame.image.load("assets/WaterDroplet.png").convert_alpha()
fuel_icon = pygame.image.load("assets/fuel.png").convert_alpha()
oxygen_icon = pygame.image.load("assets/oxygen.png").convert_alpha()

# Scale icons if needed
icon_size = (25, 25)
health_icon = pygame.transform.scale(health_icon, icon_size)
thirst_icon = pygame.transform.scale(thirst_icon, icon_size)
fuel_icon = pygame.transform.scale(fuel_icon, icon_size)
oxygen_icon = pygame.transform.scale(oxygen_icon, icon_size)

# Define bar properties
bar_width = 100
bar_height = 10
bar_x = 40  # X position after the icon
bar_y_offset = 10  # Spacing between bars
# Define tile borders
x = WIDTH // 2
y = HEIGHT // 2

diamond_center = (x, y)
diamond_size = 200

top = (x + 10, y + 100 - diamond_size)
right = (x + 20 + diamond_size, y + 10)
bottom = (x, y - 70 + diamond_size)
left = (x - 5 - diamond_size, y + 15)

diamond_points = [top, right, bottom, left]

# Create diamond mask once
diamond_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
pygame.draw.polygon(diamond_surface, (255, 255, 255), diamond_points)
diamond_mask = pygame.mask.from_surface(diamond_surface)

HUNGER_RATE = 0.05  # Hunger increases over time
THIRST_RATE = 0.07  # Thirst increases over time
FUEL_RATE = 0.1     # Fuel decreases when moving
OXYGEN_RATE = 0.03  # Oxygen decreases over time
HEALTH_RATE = 0.01

def get_exit_side(player_pos, center):
    dx = player_pos[0] - center[0]
    dy = player_pos[1] - center[1]

    angle = math.degrees(math.atan2(-dy, dx))
    angle %= 360

    if 0 <= angle < 90:
        return "top-right"
    elif 90 <= angle < 180:
        return "top-left"
    elif 180 <= angle < 270:
        return "bottom-left"
    else:
        return "bottom-right"

def draw_stat_bar(screen, icon, value, max_value, x, y, color):
    screen.blit(icon, (x - 25, y - 5))
    pygame.draw.rect(screen, (50, 50, 50), (x, y, bar_width, bar_height))
    fill_width = (value / max_value) * bar_width
    pygame.draw.rect(screen, color, (x, y, fill_width, bar_height))

def update_stats(player, moving=False, tile_type="blank"):
    player.hunger = min(player.hunger + HUNGER_RATE, 100)
    player.thirst = max(player.thirst - THIRST_RATE, 0)
    player.oxygen = max(player.oxygen - OXYGEN_RATE, 0)

    if moving:
        player.fuel = max(player.fuel - FUEL_RATE, 0)

    if player.hunger >= 100 or player.thirst >= 100:
        player.health = max(player.health - HEALTH_RATE, 0)

    if tile_type == "cave":
        player.oxygen = min(player.oxygen + 0.05, 100)
    elif tile_type == "ore":
        player.fuel = min(player.fuel + 0.02, 100)

# Game Loop
running = True
last_pos = (player.x, player.y)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(0)

    tile_image = map.tile_images[(player.map_x, player.map_y)]
    screen.blit(tile_image, (0, 0))
    screen.blit(player.image, (player.x, player.y))

    draw_stat_bar(screen, health_icon, player.health, 100, bar_x, bar_y_offset, (255, 0, 0))
    draw_stat_bar(screen, thirst_icon, player.thirst, 100, bar_x, bar_y_offset + 20, (0, 0, 255))
    draw_stat_bar(screen, fuel_icon, player.fuel, 100, bar_x, bar_y_offset + 40, (255, 255, 0))
    draw_stat_bar(screen, oxygen_icon, player.oxygen, 100, bar_x, bar_y_offset + 60, (0, 255, 0))

    current_pos = (player.x, player.y)
    moving = current_pos != last_pos
    last_pos = current_pos
    map_tile = map.get_tile(player.map_x, player.map_y)
    update_stats(player, moving, map_tile)

    player_pos = (int(player.x), int(player.y))
    if diamond_mask.get_at(player_pos):
        player.move(WIDTH, HEIGHT)
    else:
        exit_side = get_exit_side(player_pos, diamond_center)
        
        if exit_side == "top-right":
            if player.map_y < map_size:
                player.map_y += 1
                player.x = 150
                player.y = 324
            else:
                player.x -= 1
                player.y += 1
        elif exit_side == "bottom-right":
            if player.map_x < map_size:
                player.map_x += 1
                player.x = 177
                player.y = 195
            else:
                player.x -= 1
                player.y -= 1
        elif exit_side == "bottom-left":
            if player.map_y > 0:
                player.map_y -= 1
                player.x = 349
                player.y = 197
            else:
                player.x += 1
                player.y -= 1
        elif exit_side == "top-left":
            if player.map_x > 0:
                player.map_x -= 1
                player.x = 356
                player.y = 321
            else:
                player.x += 1
                player.y += 1


        print(player.map_x, player.map_y)

    if player.health <= 0:
        print("Game Over: You died!")
        running = False

    pygame.display.flip()
    clock.tick(60)
