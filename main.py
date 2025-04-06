import pygame
import sys
from character import Character
from map import Map
from item import *
import math
import time
import random
from Interactions import FarmPlot
from item import Plant
import pygame_widgets
from pygame_widgets.button import Button

# Initialisation
pygame.init()
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Marooned on Mars")

# Initialisation of Items:
fuels = {
    "Combustite": Fuel("Combustite", 1, 30, 1),
    "Ionflux": Fuel("Ionflux", 1.5, 60, 4),
    "Void Ether": Fuel("Void Ether", 2, 90, 7)
}

ores = {
    "Rustalon": Ore("Rustalon", 1, 1),
    "Hexacron": Ore("Hexacron", 1.5, 4),
    "Xerocite": Ore("Xerocite", 2, 7)
}

radioactives = {
    "Nytrazine": Radioactive("Nytrazine", 1, 1, 1),
    "Tatonium": Radioactive("Tatonium", 1.5, 4, 4),
    "Aetherium-94": Radioactive("Aetherium-94", 2, 6, 7)
}

plants = {
    "Basic Potato": Plant("Basic Potato", 0.5, 1, 1, 1),
    "Mars Potato": Plant("Mars Potato", 1, 3, 0, 0.5),
    "Tree Potato": Plant("Tree Potato", 1, 0, 3, 0.5)
}

oxygen_tanks = {
    "Oxygen Tank A": OxygenTank("Oxygen Tank A", 1, 100, 100),
    "Oxygen Tank B": OxygenTank("Oxygen Tank B", 1, 100, 100)
}

drill_bits = [
    DrillBit("Rustalon Drill Bit 1", 1),
    DrillBit("Rustalon Drill Bit 2", 2),
    DrillBit("Rustalon Drill Bit 3", 3),
    DrillBit("Hexacron Drill Bit 1", 4),
    DrillBit("Hexacron Drill Bit 2", 5),
    DrillBit("Hexacron Drill Bit 3", 6),
    DrillBit("Xerocite Drill Bit 1", 7),
    DrillBit("Xerocite Drill Bit 2", 8),
    DrillBit("Xerocite Drill Bit 3", 9)
]

batteries = [
    Battery("Potato Battery", 50),
    Battery("Spark Unit", 100),
    Battery("Pulse Pak", 200),
    Battery("Void Crystal", 300)
]

player_drill = Drill(batteries[0].battery, drill_bits[0].drill_bit)


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
    'ore': [
        pygame.image.load("assets/tile_1.png").convert_alpha(),
        pygame.image.load("assets/tile_5.png").convert_alpha(),
        pygame.image.load("assets/tile_7.png").convert_alpha(),
        pygame.image.load("assets/tile_8.png").convert_alpha()
    ],
    'ship': [pygame.image.load("assets/tile_4.png").convert_alpha()]
}

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
potato = Plant("Potato", 0.5, 20, 0, 10)  # 10 seconds to grow
radioactive_potato = Plant("Radioactive Potato", 0.5, 15, -5, 15)

player.add_item(potato)

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

HOTBAR_SLOT_SIZE = 40
HOTBAR_X = (WIDTH - (HOTBAR_SLOT_SIZE * 9)) // 2
HOTBAR_Y = HEIGHT - HOTBAR_SLOT_SIZE - 10

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

font = pygame.font.Font(None, 24)


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


def draw_hotbar(screen, player):
    for i in range(9):
        x = HOTBAR_X + (i * HOTBAR_SLOT_SIZE)
        color = (100, 100, 100) if i != player.selected_hotbar_slot else (
            200, 200, 200)
        pygame.draw.rect(screen, color, (x, HOTBAR_Y,
                         HOTBAR_SLOT_SIZE, HOTBAR_SLOT_SIZE))
        if player.hotbar[i]:
            text = font.render(player.hotbar[i].name[0], True, (255, 255, 255))
            screen.blit(text, (x + 10, HOTBAR_Y + 10))


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

current_page = 0
pages = ["menu", "location", "game"]
seedxy = []

page_change_flag = False
page_change_time = 0
delay_duration = 0.5

def change_page():
    global current_page
    current_page += 1
    if current_page >= len(pages):
        current_page = 0  # Reset to menu if needed, or handle differently
    print(f"Changed to page: {pages[current_page]}")


while running:
    # Get all events once per frame
    events = pygame.event.get()
    
    # Check for quit event in all pages
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Handle current page
    if pages[current_page] == "menu":
        button_width = 300
        button_height = 150
        inactive_col = (255, 140, 0)
        hover_col = (255, 100, 0)
        pressed_col = (200, 50, 0)

        button = Button(
            screen,
            WIDTH // 2 - button_width // 2,
            HEIGHT // 2 - button_height // 2,
            button_width,
            button_height,
            text='Play',
            fontSize=40,
            fontColour=(255, 255, 255),
            inactiveColour=inactive_col,
            hoverColour=hover_col,
            pressedColour=pressed_col,
            radius=30,
            borderThickness=3,
            borderColour=(255, 100, 0),
            onClick=lambda: change_page()
        )

        # Update widgets with the events we already collected
        pygame_widgets.update(events)
        
    elif pages[current_page] == "location":
        screen.fill(0)
        mars = pygame.image.load("assets/mars.png")
        screen.blit(mars, (0, 0))

        # Check for mouse click
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and not page_change_flag:
                x, y = pygame.mouse.get_pos()
                print(x, y)
                mars_rect = mars.get_rect()
                if mars_rect.collidepoint(x, y):
                    clicked_pixel = mars.get_at((x, y))
                    if clicked_pixel.a > 0:
                        seedxy = [x, y]
                        page_change_flag = True
                        page_change_time = time.time()

        # Wait for mouse button release
        if page_change_flag:
            if pygame.mouse.get_pressed()[0] == 0:
                if time.time() - page_change_time >= delay_duration:
                    seed = random.seed(int(str(x) + str(y)))
                    map = Map(map_size, seed, map_key)
                    map.display_map()

                    farm_plots = []
                    for mx in range(map_size):
                        for my in range(map_size):
                            if map.get_tile(mx, my) == "blank":  # Changed from "blank" to "ore"
                                farm_plots.append(FarmPlot(WIDTH/2, HEIGHT/2, mx, my))
                    change_page()
                    page_change_flag = False
                    
    elif pages[current_page] == "game":
        for event in events:
            if event.type == pygame.KEYDOWN:
                if pygame.K_1 <= event.key <= pygame.K_9:
                    player.select_hotbar(event.key - pygame.K_1)
                elif event.key == pygame.K_p:
                    current_plot = next((plot for plot in farm_plots if plot.map_x ==
                                        player.map_x and plot.map_y == player.map_y), None)
                    selected_item = player.hotbar[player.selected_hotbar_slot]
                    if current_plot and selected_item and isinstance(selected_item, Plant):
                        if current_plot.plant(selected_item):
                            player.hotbar[player.selected_hotbar_slot] = None
                elif event.key == pygame.K_h:
                    current_plot = next((plot for plot in farm_plots if plot.map_x ==
                                        player.map_x and plot.map_y == player.map_y), None)
                    if current_plot and current_plot.check_harvest():
                        harvested = current_plot.harvest()
                        if harvested and player.add_item(harvested):
                            player.hunger = max(
                                player.hunger - harvested.satiation, 0)
                            player.oxygen = min(
                                player.oxygen + harvested.oxypot, 100)

        screen.fill(0)

        tile_image = map.tile_images[(player.map_x, player.map_y)]
        screen.blit(tile_image, (0, 0))

        current_plot = next((plot for plot in farm_plots if plot.map_x == player.map_x and plot.map_y == player.map_y),
                            None)
        if current_plot and current_plot.planted_item:
            color = (0, 255, 0) if current_plot.ready else (139, 69, 19)
            pygame.draw.rect(screen, color, (WIDTH / 2 -
                             25, HEIGHT / 2 - 25, 50, 50))

        screen.blit(player.image, (player.x, player.y))

        draw_stat_bar(screen, health_icon, player.health,
                      100, bar_x, bar_y_offset, (255, 0, 0))
        draw_stat_bar(screen, thirst_icon, player.thirst, 100,
                      bar_x, bar_y_offset + 20, (0, 0, 255))
        draw_stat_bar(screen, fuel_icon, player.fuel, 100,
                      bar_x, bar_y_offset + 40, (255, 255, 0))
        draw_stat_bar(screen, oxygen_icon, player.oxygen, 100,
                      bar_x, bar_y_offset + 60, (0, 255, 0))
        draw_hotbar(screen, player)

        inv_text = "Inventory: " + \
            ", ".join(f"{k}: {v}" for k, v in player.inventory.items())
        inv_surface = font.render(inv_text, True, (255, 255, 255))
        screen.blit(inv_surface, (10, HEIGHT - 70))

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