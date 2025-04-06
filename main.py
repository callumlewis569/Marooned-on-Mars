import pygame
import sys
from character import Character
from map import Map
from item import *
import math
import time
import random
from Interactions import FarmPlot,PlacedOxygenTank
from item import Plant

# Initialisation
pygame.init()
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Marooned on Mars")

#Initialisation of Items:
fuels = {
    "Combustite": Fuel("Combustite",1,30,1),
    "Ionflux": Fuel("Ionflux",1.5,60,4),
    "Void Ether": Fuel("Void Ether",2,90,7)
}

ores = {
    "Rustalon": Ore("Rustalon",1,1),
    "Hexacron": Ore("Hexacron",1.5,4),
    "Xerocite": Ore("Xerocite",2,7)
}

radioactives = {
    "Nytrazine": Radioactive("Nytrazine",1,1,1),
    "Tatonium": Radioactive("Tatonium",1.5,4,4),
    "Aetherium-94": Radioactive("Aetherium-94",2,6,7)
}

plants = {
    "Basic Potato": Plant("Basic Potato",0.5,20,5,30),
    "Mars Potato": Plant("Mars Potato",1,30,5,60),
    "Tree Potato": Plant("Tree Potato",1,0,10,60)
}

oxygen_tanks = {
    "Oxygen Tank A": OxygenTank("Oxygen Tank A",1,0),
    "Oxygen Tank B": OxygenTank("Oxygen Tank B",1,100)
}

drill_bits = [
    DrillBit("Rustalon Drill Bit 1",1),
    DrillBit("Rustalon Drill Bit 2",2),
    DrillBit("Rustalon Drill Bit 3",3),
    DrillBit("Hexacron Drill Bit 1",4),
    DrillBit("Hexacron Drill Bit 2",5),
    DrillBit("Hexacron Drill Bit 3",6),
    DrillBit("Xerocite Drill Bit 1",7),
    DrillBit("Xerocite Drill Bit 2",8),
    DrillBit("Xerocite Drill Bit 3",9)
]

batteries = [
    Battery("Potato Battery", 50),
    Battery("Spark Unit",100),
    Battery("Pulse Pak", 200),
    Battery("Void Crystal", 300)
]

player_drill = Drill(batteries[0].battery,drill_bits[0].drill_bit)

clock = pygame.time.Clock()

# Set initial player and map features
HOTBAR_SLOT_SIZE = 40
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

player.hotbar[0] = (plants["Basic Potato"], 1)
potato_icon = pygame.image.load("assets/basic_potato.png").convert_alpha()
potato_icon = pygame.transform.scale(potato_icon, (30, 30))

player.hotbar[1] = (oxygen_tanks["Oxygen Tank A"], 1)
oxygen_tank_icon = pygame.image.load("assets/oxygen.png").convert_alpha()
oxygen_tank_icon = pygame.transform.scale(oxygen_tank_icon, (30, 30))

farm_plots = []
placed_oxygen_tanks = []

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

start_ticks = pygame.time.get_ticks()  # Start time for clock
hour = 0
day = 1


def update_game_time():
    global hour, day, start_ticks

    elapsed_time = pygame.time.get_ticks() - start_ticks

    if elapsed_time >= 20000:
        start_ticks = pygame.time.get_ticks()
        hour += 1

        if hour == 24:
            hour = 0
            day += 1

def draw_clock(screen):
    time_text = f"Day {day} | {hour:02}:00"
    time_surface = font.render(time_text, True, (255, 255, 255))  # White color for text
    screen.blit(time_surface, (WIDTH - 150, 10))  # Draw in the top-right corner

def is_near_plant(player, plant, radius=50):
    return abs(plant.x - player.x) < radius and abs(plant.y - player.y) < radius

def draw_growth_bar(screen, plot):
    if plot and plot.planted_item and not plot.ready:
        growth_time = time.time() - plot.plant_time
        progress = min(growth_time / plot.planted_item.grow_rate, 1.0)
        bar_width = 100
        bar_height = 10

        bar_x, bar_y = plot.x, plot.y
        pygame.draw.rect(screen, (50, 50, 50), (bar_x-50, bar_y, bar_width, bar_height))
        fill_width = progress * bar_width
        pygame.draw.rect(screen, (0, 255, 0), (bar_x-50, bar_y, fill_width, bar_height))

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

def draw_hotbar(screen, player, font):
    for i in range(9):
        x = HOTBAR_X + (i * HOTBAR_SLOT_SIZE)
        color = (100, 100, 100) if i != player.selected_hotbar_slot else (200, 200, 200)
        pygame.draw.rect(screen, color, (x, HOTBAR_Y, HOTBAR_SLOT_SIZE, HOTBAR_SLOT_SIZE))
        item, count = player.hotbar[i]
        if item:
            if isinstance(item, OxygenTank):
                screen.blit(oxygen_tank_icon, (x + 5, HOTBAR_Y + 5))
                oxygen_text = f"{int(item.oxygen)}/{item.oxygen_cap}"
                text = font.render(oxygen_text, True, (255, 255, 255))
                screen.blit(text, (x + 5, HOTBAR_Y + 20))
            elif isinstance(item, Plant):
                screen.blit(potato_icon, (x + 5, HOTBAR_Y + 5))
                if count > 1:
                    count_text = font.render(str(count), True, (255, 255, 255))
                    screen.blit(count_text, (x + 25, HOTBAR_Y + 25))


def draw_stat_bar(screen, icon, value, max_value, x, y, color):
    screen.blit(icon, (x - 25, y - 5))
    pygame.draw.rect(screen, (50, 50, 50), (x, y, bar_width, bar_height))
    fill_width = (value / max_value) * bar_width
    pygame.draw.rect(screen, color, (x, y, fill_width, bar_height))


def update_stats(player, moving=False, tile_type="blank"):
    player.hunger = min(player.hunger + HUNGER_RATE, 100)
    player.thirst = max(player.thirst - THIRST_RATE, 0)

    # Check if player has an oxygen tank selected and use it
    item, count = player.hotbar[player.selected_hotbar_slot]
    oxygen_from_tank = 0
    if item and isinstance(item, OxygenTank) and item.oxygen > 0:
        oxygen_needed = min(OXYGEN_RATE, item.oxygen)  # Only take what's needed or available
        oxygen_from_tank = oxygen_needed
        item.oxygen = max(item.oxygen - oxygen_needed, 0)

    player.oxygen = max(player.oxygen - OXYGEN_RATE + oxygen_from_tank, 0)

    if player.oxygen <= 0:
        player.health = max(player.health - HEALTH_RATE, 0)

    if player.hunger >= 100 or player.thirst <= 0:
        player.health = max(player.health - HEALTH_RATE, 0)

    # Oxygen from nearby growing plants
    current_plot = next((plot for plot in farm_plots if plot.map_x == player.map_x and plot.map_y == player.map_y),
                        None)
    if current_plot and current_plot.planted_item and not current_plot.ready:
        plant_oxygen = current_plot.planted_item.oxypot / 60
        player.oxygen = min(player.oxygen + plant_oxygen, 100)

        # Add oxygen to selected tank if near plant
        if item and isinstance(item, OxygenTank):
            if abs(current_plot.x - player.x) < 50 and abs(current_plot.y - player.y) < 50:
                item.add_oxygen(plant_oxygen)

def update_oxygen_near_plants():
    for placed_tank in placed_oxygen_tanks:
        for plot in farm_plots:
            if abs(plot.x - placed_tank.x) < 50 and abs(plot.y - placed_tank.y) < 50:
                if plot.planted_item:
                    placed_tank.add_oxygen(plot.planted_item.oxypot / 60)


def update_game():
    for placed_tank in placed_oxygen_tanks[:]:  # Use a copy to allow removal
        # Check if player is near the tank and presses 'E' to pick it up
        if (abs(player.x - placed_tank.x) < 50 and
            abs(player.y - placed_tank.y) < 50 and
            pygame.key.get_pressed()[pygame.K_e]):
            if player.add_item(placed_tank):  # Add tank back to inventory
                placed_oxygen_tanks.remove(placed_tank)

# Game loop
last_pos = (player.x, player.y)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if pygame.K_1 <= event.key <= pygame.K_9:
                player.select_hotbar(event.key - pygame.K_1)

            elif event.key == pygame.K_d:
                item, count = player.hotbar[player.selected_hotbar_slot]
                if item and isinstance(item, OxygenTank) and count > 0:
                    nearby_tank = next((tank for tank in placed_oxygen_tanks
                                      if abs(tank.x - player.x) < 50 and
                                      abs(tank.y - player.y) < 50), None)
                    if nearby_tank:
                        if player.add_item(nearby_tank):
                            placed_oxygen_tanks.remove(nearby_tank)
                    else:
                        placed_tank = PlacedOxygenTank(
                            player.x,
                            player.y,
                            player.map_x,
                            player.map_y,
                            item.item_name,
                            item.item_weight,
                            item.oxygen_cap,
                            item.oxygen
                        )
                        placed_oxygen_tanks.append(placed_tank)
                        player.remove_item(player.selected_hotbar_slot)
                        
            elif event.key == pygame.K_p:
                item, count = player.hotbar[player.selected_hotbar_slot]
                if item and isinstance(item, Plant) and count > 0:
                    new_plot = FarmPlot(player.x, player.y, player.map_x, player.map_y)
                    if new_plot.plant(item):
                        player.remove_item(player.selected_hotbar_slot)
                        farm_plots.append(new_plot)

            elif event.key == pygame.K_h:
                for plot in farm_plots[:]:  # Copy list to allow removal
                    if (plot.map_x == player.map_x and plot.map_y == player.map_y and
                        abs(plot.x - player.x) < 50 and abs(plot.y - player.y) < 50 and
                        plot.check_harvest()):
                        harvested = plot.harvest()
                        if harvested:
                            for new_plant in harvested:
                                player.add_item(new_plant)
                            farm_plots.remove(plot)

    screen.fill(0)
    update_game()
    update_stats(player)
    update_oxygen_near_plants()
    update_game_time()
    draw_clock(screen)
    tile_image = map.tile_images[(player.map_x, player.map_y)]
    screen.blit(tile_image, (0, 0))

    # Draw farm plots (existing code)
    for plot in farm_plots:
        if plot.map_x == player.map_x and plot.map_y == player.map_y:
            color = (0, 255, 0) if plot.ready else (139, 69, 19)
            pygame.draw.rect(screen, color, (plot.x - 15, plot.y - 15, 30, 30))
            draw_growth_bar(screen, plot)

    # Draw only oxygen tanks on current map tile
    for tank in placed_oxygen_tanks:
        if tank.map_x == player.map_x and tank.map_y == player.map_y:
            tank.draw(screen, font)
    screen.blit(player.image, (player.x, player.y))

    draw_stat_bar(screen, health_icon, player.health, 100, bar_x, bar_y_offset, (255, 0, 0))
    draw_stat_bar(screen, thirst_icon, player.thirst, 100, bar_x, bar_y_offset + 20, (0, 0, 255))
    draw_stat_bar(screen, fuel_icon, player.fuel, 100, bar_x, bar_y_offset + 40, (255, 255, 0))
    draw_stat_bar(screen, oxygen_icon, player.oxygen, 100, bar_x, bar_y_offset + 60, (0, 255, 0))
    draw_hotbar(screen, player, font)

    inv_text = "Inventory: " + ", ".join(f"{k}: {v}" for k, v in player.inventory.items())
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
