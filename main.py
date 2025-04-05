import pygame
import sys
from character import Character
from map import Map
import math
import time

# Initialisation
pygame.init()
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Marooned on Mars")

clock = pygame.time.Clock()

# Set initial player and map features
map_size = 10
map = Map(map_size, 0)

map_key = {
    'blank': pygame.image.load("assets/tile_1.png").convert_alpha(),
    'mountain': pygame.image.load("assets/tile_2.png").convert_alpha(),
    'cave': pygame.image.load("assets/tile_3.png").convert_alpha(),
    'ore': pygame.image.load("assets/tile_4.png").convert_alpha()
}

map.print_map()

player_x = WIDTH / 2
player_y = HEIGHT / 2
map_x = map_size // 2
map_y = map_size // 2
player_speed = 1
player_hunger = 0
player_thirst = 0
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
pygame.font.init()
my_font = pygame.font.SysFont('Times New Roman', 15)
hunger_text = my_font.render(
    f'Hunger: {player.hunger}', False, (255, 255, 255))
thirst_text = my_font.render(
    f'Thirst: {player.thirst}', False, (255, 255, 255))
fuel_text = my_font.render(f'Fuel: {player.fuel}', False, (255, 255, 255))
oxygen_text = my_font.render(
    f'Oxygen: {player.oxygen}', False, (255, 255, 255))

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

# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(0)

    map_tile = map.get_tile(player.map_x, player.map_y)
    screen.blit(map_key[map_tile], (0, 0))
    screen.blit(player.image, (player.x, player.y))
    screen.blit(hunger_text, (10, 0))
    screen.blit(thirst_text, (10, 20))
    screen.blit(fuel_text, (10, 40))
    screen.blit(oxygen_text, (10, 60))

    # Check if player is inside the diamond shape
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

    pygame.display.flip()
    clock.tick(60)
