import pygame
import sys
from character import Character
from map import Map
import item
import math
import time
import random
from Interactions import FarmPlot, PlacedOxygenTank
from item import Plant
import pygame_widgets
from pygame_widgets.button import Button
from ai_assistant import Shannon
import asyncio
import pyaudio

# Initialisation
pygame.init()
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Marooned on Mars")

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

player_x = 206
player_y = 296
map_x = map_size // 2
map_y = map_size // 2
player_speed = 1
player_hunger = 100
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

# Display text
health_icon = pygame.image.load("assets/heart.png").convert_alpha()
thirst_icon = pygame.image.load("assets/WaterDroplet.png").convert_alpha()
fuel_icon = pygame.image.load("assets/fuel.png").convert_alpha()
oxygen_icon = pygame.image.load("assets/oxygen.png").convert_alpha()
food_icon = pygame.image.load("assets/food_icon.png").convert_alpha()

# Scale icons if needed
icon_size = (25, 25)
health_icon = pygame.transform.scale(health_icon, icon_size)
thirst_icon = pygame.transform.scale(thirst_icon, icon_size)
fuel_icon = pygame.transform.scale(fuel_icon, icon_size)
oxygen_icon = pygame.transform.scale(oxygen_icon, icon_size)
food_icon = pygame.transform.scale(food_icon, (20, 20))

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

HUNGER_RATE = 0.005  # Hunger increases over time
THIRST_RATE = 0.01  # Thirst increases over time
FUEL_RATE = 0.02     # Fuel decreases when moving
OXYGEN_RATE = 0.007  # Oxygen decreases over time
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
    time_surface = font.render(
        time_text, True, (255, 255, 255))  # White color for text
    # Draw in the top-right corner
    screen.blit(time_surface, (WIDTH - 150, 10))

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
    player.hunger = min(player.hunger - HUNGER_RATE, 100)
    player.thirst = max(player.thirst - THIRST_RATE, 0)    
    player.oxygen = max(player.oxygen - OXYGEN_RATE, 0)

    # Health effects
    if player.oxygen <= 0:
        player.health = max(player.health - HEALTH_RATE, 0)

    if player.hunger >= 100 or player.thirst <= 0:
        player.health = max(player.health - HEALTH_RATE, 0)

# Game loop


current_page = 0
pages = ["menu", "location", "game"]


page_change_flag = False
page_change_time = 0
delay_duration = 0.5


def change_page():
    global current_page
    current_page += 1
    if current_page >= len(pages):
        current_page = 0  # Reset to menu if needed, or handle differently
    print(f"Changed to page: {pages[current_page]}")


async def game_loop():
    global stop_flag
    running = True
    seedxy = []
    inside_ship = False
    last_pos = (player.x, player.y)
    agent_task = None

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

            if seedxy:
                cross = pygame.image.load("assets/cross.png")
                screen.blit(cross, (seedxy[0] - 10.5, seedxy[1] - 10.5))

                # Create a confirmation button
                button_width = 150
                button_height = 50
                button_x = WIDTH - button_width - 20
                button_y = HEIGHT - button_height - 20

                # Draw the button
                pygame.draw.rect(screen, (0, 200, 0), (button_x,
                                                       button_y, button_width, button_height), 0, 10)

                # Draw button text
                confirm_text = font.render("Confirm", True, (255, 255, 255))
                text_rect = confirm_text.get_rect(
                    center=(button_x + button_width/2, button_y + button_height/2))
                screen.blit(confirm_text, text_rect)

                # Check if the confirm button is clicked
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if button_x <= mouse_pos[0] <= button_x + button_width and button_y <= mouse_pos[1] <= button_y + button_height:
                            # Initialize game with the selected seed
                            x, y = seedxy
                            seed = random.seed(int(str(x) + str(y)))
                            map = Map(map_size, seed, map_key)
                            map.display_map()

                            change_page()
                            page_change_flag = False

            # Handle new clicks on the map
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    mars_rect = mars.get_rect()
                    if mars_rect.collidepoint(x, y):
                        clicked_pixel = mars.get_at((x, y))
                        if clicked_pixel.a > 0:
                            seedxy = [x, y]
                            # No longer setting page_change_flag here since we're using the confirm button

        elif pages[current_page] == "game":
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:  # Press 'q' to quit the agent
                        print("Quitting the AI agent...")
                        agent_task.cancel()  # Cancel the agent task
                        inside_ship = False

            screen.fill(0)

            if inside_ship:
                if day < 3 and agent_task is None:
                    shannon = Shannon(player.oxygen, player.thirst, player.hunger,
                  player.fuel, 100, player.inventory)
                    agent_task = asyncio.create_task(shannon.good())
                elif day < 7 and agent_task is None:
                    shannon = Shannon(player.oxygen, player.thirst, player.hunger,
                  player.fuel, 100, player.inventory)
                    agent_task = asyncio.create_task(shannon.middle())
                elif day >= 7 and agent_task is None:
                    shannon = Shannon(player.oxygen, player.thirst, player.hunger,
                  player.fuel, 100, player.inventory)
                    agent_task = asyncio.create_task(shannon.evil())
            
            # If player leaves the ship, cancel the agent task
            if not inside_ship and agent_task:
                agent_task.cancel()
                agent_task = None  # Reset the agent task reference

            if ((player.map_x == map_size // 2 and player.map_y == map_size // 2)
                    and (player.x < 280 and player.x > 235 and player.y > 272 and player.y < 292)):
                inside_ship = True

            

            
            if not inside_ship:
                update_stats(player)
                update_game_time()
                draw_clock(screen)
            tile_image = pygame.image.load(
                "assets/ship_interior.png") if inside_ship else map.tile_images[(player.map_x, player.map_y)]
            screen.blit(tile_image, (0, 0))

            draw_stat_bar(screen, health_icon, player.health,
                          100, bar_x, bar_y_offset, (255, 0, 0))
            draw_stat_bar(screen, thirst_icon, player.thirst, 100,
                          bar_x, bar_y_offset + 20, (0, 0, 255))
            draw_stat_bar(screen, fuel_icon, player.fuel, 100,
                          bar_x, bar_y_offset + 40, (255, 255, 0))
            draw_stat_bar(screen, oxygen_icon, player.oxygen, 100,
                          bar_x, bar_y_offset + 60, (0, 255, 0))
            draw_stat_bar(screen, food_icon, player.hunger, 100,
                          bar_x, bar_y_offset + 80, (120, 0, 0))
            # draw_hotbar(screen, player, font)

            screen.blit(player.image, (player.x, player.y))

            draw_stat_bar(screen, health_icon, player.health,
                          100, bar_x, bar_y_offset, (255, 0, 0))
            draw_stat_bar(screen, thirst_icon, player.thirst, 100,
                          bar_x, bar_y_offset + 20, (0, 0, 255))
            draw_stat_bar(screen, fuel_icon, player.fuel, 100,
                          bar_x, bar_y_offset + 40, (255, 255, 0))
            draw_stat_bar(screen, oxygen_icon, player.oxygen, 100,
                          bar_x, bar_y_offset + 60, (0, 255, 0))

            current_pos = (player.x, player.y)
            moving = current_pos != last_pos
            last_pos = current_pos
            map_tile = map.get_tile(player.map_x, player.map_y)
            update_stats(player, moving, map_tile)

            player_pos = (int(player.x), int(player.y))
            if diamond_mask.get_at(player_pos) or inside_ship:
                player.move(WIDTH, HEIGHT)
            else:
                exit_side = get_exit_side(player_pos, diamond_center)

                if exit_side == "top-right":
                    if player.map_y < map_size - 1:
                        player.map_y += 1
                        player.x = 150
                        player.y = 324
                    else:
                        player.x -= 1
                        player.y += 1
                elif exit_side == "bottom-right":
                    if player.map_x < map_size - 1:
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

            if player.health <= 0:
                print("Game Over: You died!")
                running = False

        await asyncio.sleep(0.01)
        pygame.display.flip()
        clock.tick(60)


async def main():
    await game_loop()

if __name__ == "__main__":
    asyncio.run(main())
