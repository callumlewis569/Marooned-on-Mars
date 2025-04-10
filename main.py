import pygame
import sys
from character import Character
from map import Map
import item
import math
import time
import random
from Interactions import  PlacedOxygenTank, PlacedPlant
from item import Plant, OxygenTank
import pygame_widgets
from pygame_widgets.button import Button
from ai_assistant import Shannon
import asyncio
import pyaudio


class GameState:
    """Base class for all game states"""

    def __init__(self, game):
        self.game: Game = game

    def handle_events(self, events):
        """Process pygame events"""
        pass

    def update(self, dt):
        """Update game logic"""
        pass

    def render(self):
        """Render the state to the screen"""
        pass

    def enter(self, **kwargs):
        """Called when state becomes active"""
        pass

    def exit(self):
        """Called when state is no longer active"""
        pass


class MenuState(GameState):
    """Main menu state"""

    def __init__(self, game):
        super().__init__(game)
        self.button = None

    def enter(self, **kwargs):
        # Setup menu elements
        button_width = 300
        button_height = 150
        inactive_col = (255, 140, 0)
        hover_col = (255, 100, 0)
        pressed_col = (200, 50, 0)

        self.button = Button(
            self.game.screen,
            self.game.WIDTH // 2 - button_width // 2,
            self.game.HEIGHT // 2 - button_height // 2,
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
            onClick=lambda: self.game.change_state("location")
        )

    def handle_events(self, events):
        pygame_widgets.update(events)

    def render(self, **kwargs):
        self.game.screen.fill(0)  # Clear screen with black
        events = kwargs['events']
        pygame_widgets.update(events)


class LocationSelectionState(GameState):
    """State for selecting spawn location on Mars"""

    def __init__(self, game):
        super().__init__(game)
        self.mars_surface = pygame.image.load("assets/mars.png")
        self.cross_icon = pygame.image.load("assets/cross.png")
        self.selected_point = None
        self.confirm_button_rect = None

    def enter(self, **kwargs):
        self.selected_point = None

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Check for clicks on the Mars surface
                mars_rect = self.mars_surface.get_rect()
                if mars_rect.collidepoint(mouse_pos):
                    clicked_pixel = self.mars_surface.get_at(mouse_pos)
                    if clicked_pixel.a > 0:  # Ensure it's not clicking on transparent part
                        self.selected_point = list(mouse_pos)

                # Check for confirm button click if location is selected
                if self.selected_point and self.confirm_button_rect:
                    if self.confirm_button_rect.collidepoint(mouse_pos):
                        # Initialize the game map with the selected seed
                        x, y = self.selected_point
                        seed = random.seed(int(str(x) + str(y)))
                        self.game.initialize_map(seed)
                        self.game.change_state("gameplay")

    def render(self, **_):
        self.game.screen.fill(0)
        self.game.screen.blit(self.mars_surface, (0, 0))

        if self.selected_point:
            # Draw selection cross
            self.game.screen.blit(
                self.cross_icon, (self.selected_point[0] - 10.5, self.selected_point[1] - 10.5))

            # Draw confirmation button
            button_width = 150
            button_height = 50
            button_x = self.game.WIDTH - button_width - 20
            button_y = self.game.HEIGHT - button_height - 20

            self.confirm_button_rect = pygame.Rect(
                button_x, button_y, button_width, button_height)
            pygame.draw.rect(self.game.screen, (0, 200, 0),
                             self.confirm_button_rect, 0, 10)

            # Draw button text
            confirm_text = self.game.font.render(
                "Confirm", True, (255, 255, 255))
            text_rect = confirm_text.get_rect(
                center=(button_x + button_width/2, button_y + button_height/2))
            self.game.screen.blit(confirm_text, text_rect)


class GameplayState(GameState):
    """Main gameplay state"""

    def __init__(self, game):
        super().__init__(game)
        self.last_pos = None

    def enter(self, **_):
        pass

    def exit(self):
        pass

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                # Inventory selection
                if pygame.K_1 <= event.key <= pygame.K_9:
                    slot = event.key - pygame.K_1
                    self.game.player.select_inventory(slot)
                    print(
                        f"Selected inventory slot {slot + 1}: {self.game.player.inventory[slot]}")
                elif event.key == pygame.K_p:
                    self.pressing_p()
                elif event.key == pygame.K_h:
                    self.pressing_h()
                elif event.key == pygame.K_u:
                    self.pressing_u()
                # Add escape key to return to menu
                if event.key == pygame.K_ESCAPE:
                    self.game.change_state("menu")

    def pressing_u(self):
        selected_slot = self.game.player.selected_inventory_slot
        item, count = self.game.player.inventory[selected_slot]
        if isinstance(item, OxygenTank):
            for tank in self.game.player.transferring_tanks[:]:
                if tank.oxygen > 0:
                    tank.transfer_oxygen(self.game.player) 
        elif isinstance(item, Plant):
            if count > 0 and self.game.player.hunger < self.game.player.hunger_cap:
                item.eat(self.game.player, selected_slot)
            else:
                print("You are already full! You can't eat more.")

    def pressing_p(self):
        selected_slot = self.game.player.selected_inventory_slot
        item, count = self.game.player.inventory[selected_slot]
        if count >= 1:
            if isinstance(item, Plant):
                # Place the plant in the world
                placed = PlacedPlant(self.game.player.x, self.game.player.y, self.game.player.map_x,
                                     self.game.player.map_y, item, game)
                self.game.planted_crops.append(placed)

                # Decrease item count
                if count == 1:
                    self.game.player.inventory[selected_slot] = (None, 0)
                else:
                    self.game.player.inventory[selected_slot] = (item, count - 1)
                print(f"Planted {item.name} at ({self.game.player.x}, {self.game.player.y})")

            if isinstance(item, OxygenTank):
                placed = PlacedOxygenTank(self.game.player.x, self.game.player.y, self.game.player.map_x,
                                          self.game.player.map_y, item, game, self.game.player)
                self.game.oxygen_tanks.append(placed)
                # Decrease item count
                if count == 1:
                    self.game.player.inventory[selected_slot] = (None, 0)
                else:
                    self.game.player.inventory[selected_slot] = (item, count - 1)
                print(f"Planted {item.name} at ({self.game.player.x}, {self.game.player.y})")

    def pressing_h(self):
        for plant in self.game.planted_crops[:]:
            plant.check_harvest()
            if plant.ready:
                distance = math.hypot(self.game.player.x - plant.x, self.game.player.y - plant.y)
                if distance < 40:
                    harvested_items = plant.harvest()
                    for item in harvested_items:
                        self.game.player.add_item(item)
                    self.game.planted_crops.remove(plant)

        for tank in self.game.oxygen_tanks[:]:
            distance = math.hypot(self.game.player.x - tank.x, self.game.player.y - tank.y)
            if distance < 40:
                picked_up_tank = tank.pickup()
                if self.game.player.add_item(picked_up_tank):
                    self.game.oxygen_tanks.remove(tank)
                    print(
                        f"Picked up {picked_up_tank.name} with {picked_up_tank.oxygen}/{picked_up_tank.oxygen_cap} O2")
                    if picked_up_tank.oxygen > 0:
                        self.game.player.transferring_tanks.append(picked_up_tank)
                else:
                    print("Inventory full!")

    def update(self, _):
        # Check if player is inside the ship
        self.check_ship_proximity()

        # Update game time
        self.game.update_game_time()

        # Update player movement and position
        current_pos = (self.game.player.x, self.game.player.y)
        moving = current_pos != self.last_pos
        self.last_pos = current_pos

        # Get current tile and update stats
        map_tile = self.game.map.get_tile(
            self.game.player.map_x, self.game.player.map_y)
        self.game.update_stats(moving, map_tile)

        # Handle player movement and map transitions
        self.handle_player_movement()

        # Check game over condition
        if self.game.player.health <= 0:
            print("Game Over: You died!")
            self.game.change_state("menu")

    def check_ship_proximity(self):
        # Check if player is in the ship's location and inside the entry area
        if ((self.game.player.map_x == self.game.map_size // 2 and
             self.game.player.map_y == self.game.map_size // 2) and
            (self.game.player.x < 280 and self.game.player.x > 235 and
             self.game.player.y > 272 and self.game.player.y < 292)):
            self.game.change_state("spaceship")

    def handle_player_movement(self):
        player_pos = (int(self.game.player.x), int(self.game.player.y))

        # Check if player is within the diamond boundary
        if self.game.diamond_mask.get_at(player_pos):
            self.game.player.move(self.game.WIDTH, self.game.HEIGHT)
        else:
            # Player is leaving the current tile
            exit_side = self.game.get_exit_side(
                player_pos, self.game.diamond_center)

            if exit_side == "top-right":
                if self.game.player.map_y < self.game.map_size - 1:
                    self.game.player.map_y += 1
                    self.game.player.x = 150
                    self.game.player.y = 324
                else:
                    self.game.player.x -= 1
                    self.game.player.y += 1
            elif exit_side == "bottom-right":
                if self.game.player.map_x < self.game.map_size - 1:
                    self.game.player.map_x += 1
                    self.game.player.x = 177
                    self.game.player.y = 195
                else:
                    self.game.player.x -= 1
                    self.game.player.y -= 1
            elif exit_side == "bottom-left":
                if self.game.player.map_y > 0:
                    self.game.player.map_y -= 1
                    self.game.player.x = 349
                    self.game.player.y = 197
                else:
                    self.game.player.x += 1
                    self.game.player.y -= 1
            elif exit_side == "top-left":
                if self.game.player.map_x > 0:
                    self.game.player.map_x -= 1
                    self.game.player.x = 356
                    self.game.player.y = 321
                else:
                    self.game.player.x += 1
                    self.game.player.y += 1

    def render(self, **_):
        self.game.screen.fill(0)

        # Render current tile
        tile_image = self.game.map.tile_images[(
            self.game.player.map_x, self.game.player.map_y)]
        self.game.screen.blit(tile_image, (0, 0))

        for plant in self.game.planted_crops:
            if (plant.map_x, plant.map_y) == (self.game.player.map_x, self.game.player.map_y):
                plant.check_harvest()
                plant.draw(self.game.screen)


        for tank in self.game.oxygen_tanks:
            if (tank.map_x, tank.map_y) == (self.game.player.map_x, self.game.player.map_y):
                tank.check_near_plant()
                tank.draw(self.game.screen, self.game.font)

        # Draw UI elements
        self.render_ui()

        # Draw player
        self.game.screen.blit(self.game.player.image,
                              (self.game.player.x, self.game.player.y))

    def render_ui(self):
        # Draw stat bars
        self.game.draw_stat_bar(self.game.health_icon, self.game.player.health,
                                100, self.game.bar_x, self.game.bar_y_offset, (255, 0, 0))
        self.game.draw_stat_bar(self.game.thirst_icon, self.game.player.thirst, 100,
                                self.game.bar_x, self.game.bar_y_offset + 20, (0, 0, 255))
        self.game.draw_stat_bar(self.game.fuel_icon, self.game.player.fuel, 100,
                                self.game.bar_x, self.game.bar_y_offset + 40, (255, 255, 0))
        self.game.draw_stat_bar(self.game.oxygen_icon, self.game.player.oxygen, 100,
                                self.game.bar_x, self.game.bar_y_offset + 60, (0, 255, 0))
        self.game.draw_stat_bar(self.game.food_icon, self.game.player.hunger, 100,
                                self.game.bar_x, self.game.bar_y_offset + 80, (120, 0, 0))

        # Draw inventory
        self.game.draw_inventory()

        # Draw clock
        self.game.draw_clock()


class SpaceShipState(GameState):
    """State for when inside the spaceship"""

    def __init__(self, game):
        super().__init__(game)
        self.last_pos = None
        self.agent_task = None

    def enter(self):
        self.last_pos = (self.game.player.x, self.game.player.y)
        self.agent_task = None

    def exit(self):
        # Cancel any running agent task when exiting gameplay
        if self.agent_task:
            self.agent_task.cancel()
            self.agent_task = None

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:  # Press 'q' to quit the agent
                    print("Quitting the AI agent...")
                    if self.agent_task:
                        self.agent_task.cancel()
                    self.game.change_state("gameplay")

    def update(self, _):
        # Update AI assistant based on ship status
        self.update_ai_assistant()

        # Update game time
        self.game.update_game_time()

        # Update player movement and position
        current_pos = (self.game.player.x, self.game.player.y)
        moving = current_pos != self.last_pos
        self.last_pos = current_pos

        # Get current tile and update stats
        map_tile = self.game.map.get_tile(
            self.game.player.map_x, self.game.player.map_y)
        self.game.update_stats(moving, map_tile)

        # Handle player movement and map transitions
        self.game.player.move(self.game.WIDTH, self.game.HEIGHT)

        # Check game over condition
        if self.game.player.health <= 0:
            print("Game Over: You died!")
            self.game.change_state("menu")

    def update_ai_assistant(self):
        # If player is inside the ship, activate the AI assistant based on game progress
        if self.game.day < 3 and self.agent_task is None:
            shannon = Shannon(self.game.player.oxygen, self.game.player.thirst,
                              self.game.player.hunger, self.game.player.fuel,
                              100, self.game.player.inventory)
            self.agent_task = asyncio.create_task(shannon.good())
        elif self.game.day < 7 and self.agent_task is None:
            shannon = Shannon(self.game.player.oxygen, self.game.player.thirst,
                              self.game.player.hunger, self.game.player.fuel,
                              100, self.game.player.inventory)
            self.agent_task = asyncio.create_task(shannon.middle())
        elif self.game.day >= 7 and self.agent_task is None:
            shannon = Shannon(self.game.player.oxygen, self.game.player.thirst,
                              self.game.player.hunger, self.game.player.fuel,
                              100, self.game.player.inventory)
            self.agent_task = asyncio.create_task(shannon.evil())

    def render(self, **_):
        # Render current tile
        tile_image = pygame.image.load("assets/ship_interior.png")
        self.game.screen.blit(tile_image, (0, 0))

        # Draw UI elements
        self.render_ui()

        # Draw player
        self.game.screen.blit(self.game.player.image,
                              (self.game.player.x, self.game.player.y))

    def render_ui(self):
        # Draw stat bars
        self.game.draw_stat_bar(self.game.health_icon, self.game.player.health,
                                100, self.game.bar_x, self.game.bar_y_offset, (255, 0, 0))
        self.game.draw_stat_bar(self.game.thirst_icon, self.game.player.thirst, 100,
                                self.game.bar_x, self.game.bar_y_offset + 20, (0, 0, 255))
        self.game.draw_stat_bar(self.game.fuel_icon, self.game.player.fuel, 100,
                                self.game.bar_x, self.game.bar_y_offset + 40, (255, 255, 0))
        self.game.draw_stat_bar(self.game.oxygen_icon, self.game.player.oxygen, 100,
                                self.game.bar_x, self.game.bar_y_offset + 60, (0, 255, 0))
        self.game.draw_stat_bar(self.game.food_icon, self.game.player.hunger, 100,
                                self.game.bar_x, self.game.bar_y_offset + 80, (120, 0, 0))

        # Draw inventory
        self.game.draw_inventory()

        # Draw clock
        self.game.draw_clock()


class Game:
    """Main game class that manages all game states"""
    # Constants
    WIDTH, HEIGHT = 500, 500
    HUNGER_RATE = 0.005
    THIRST_RATE = 0.01
    FUEL_RATE = 0.02
    OXYGEN_RATE = 0.007
    HEALTH_RATE = 0.01

    def __init__(self):
        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Marooned on Mars")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.planted_crops = []
        self.oxygen_tanks = []

        # Initialize game components
        self.initialize_player()
        self.load_assets()
        self.create_diamond_mask()
        self.initialize_time()
        self.initialize_inventory_settings()


        # Create state dictionary
        self.states = {
            "menu": MenuState(self),
            "location": LocationSelectionState(self),
            "gameplay": GameplayState(self),
            "spaceship": SpaceShipState(self)
        }

        # Set initial state
        self.current_state = None
        self.map = None

        # Change to initial state
        self.change_state("menu")

    def initialize_player(self):
        """Initialize player character and stats"""
        self.map_size = 10

        # Player starting position and stats
        player_x, player_y = 206, 296
        map_x, map_y = self.map_size // 2, self.map_size // 2
        player_speed = 1
        player_hunger = 100
        player_thirst = 100
        player_fuel = 100
        player_oxygen = 100
        player_health = 100

        self.player = Character(
            player_x, player_y, map_x, map_y,
            player_speed, player_hunger, player_thirst,
            player_fuel, player_oxygen, player_health
        )

    def load_assets(self):
        """Load and initialize game assets"""
        # Load map tile images
        self.map_key = {
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

        # Load UI icons
        icon_size = (25, 25)
        self.health_icon = pygame.transform.scale(
            pygame.image.load("assets/heart.png").convert_alpha(), icon_size)
        self.thirst_icon = pygame.transform.scale(
            pygame.image.load("assets/WaterDroplet.png").convert_alpha(), icon_size)
        self.fuel_icon = pygame.transform.scale(
            pygame.image.load("assets/fuel.png").convert_alpha(), icon_size)
        self.oxygen_icon = pygame.transform.scale(
            pygame.image.load("assets/oxygen.png").convert_alpha(), icon_size)
        self.food_icon = pygame.transform.scale(
            pygame.image.load("assets/food_icon.png").convert_alpha(), (20, 20))

        # Define bar properties
        self.bar_width = 100
        self.bar_height = 10
        self.bar_x = 40  # X position after the icon
        self.bar_y_offset = 10  # Spacing between bars

    def create_diamond_mask(self):
        """Create the diamond-shaped movement area mask"""
        x = self.WIDTH // 2
        y = self.HEIGHT // 2

        self.diamond_center = (x, y)
        diamond_size = 200

        top = (x + 10, y + 100 - diamond_size)
        right = (x + 20 + diamond_size, y + 10)
        bottom = (x, y - 70 + diamond_size)
        left = (x - 5 - diamond_size, y + 15)

        diamond_points = [top, right, bottom, left]

        # Create diamond mask
        self.diamond_surface = pygame.Surface(
            (self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        pygame.draw.polygon(self.diamond_surface,
                            (255, 255, 255), diamond_points)
        self.diamond_mask = pygame.mask.from_surface(self.diamond_surface)

    def initialize_time(self):
        """Initialize game time"""
        self.start_ticks = pygame.time.get_ticks()
        self.hour = 0
        self.day = 1

    def initialize_inventory_settings(self):
        """Initialize inventory UI settings"""
        self.INVENTORY_SLOT_SIZE = 40
        self.INVENTORY_Y = self.HEIGHT - self.INVENTORY_SLOT_SIZE - 10
        self.INVENTORY_X = (self.WIDTH - (self.INVENTORY_SLOT_SIZE * 9)) // 2

        # Add initial items to player inventory
        self.player.add_item(item.plants["Basic Potato"])
        self.player.add_item(item.plants["Basic Potato"])
        self.player.add_item(item.plants["Mars Potato"])
        self.player.add_item(item.oxygen_tanks["Oxygen Tank A"])
        self.player.add_item(item.plants["Tree Potato"])
        self.player.add_item(item.oxygen_tanks["Oxygen Tank B"])
        self.player.add_item(item.radioactives["Nytrazine"])

    def initialize_map(self, seed):
        """Initialize the game map with a specific seed"""
        self.map = Map(self.map_size, seed, self.map_key)
        self.map.display_map()

    def change_state(self, state_name, **kwargs):
        """Change to a different game state"""
        if state_name in self.states:
            if self.current_state:
                self.current_state.exit()
            self.current_state = self.states[state_name]
            self.current_state.enter(**kwargs)
            print(f"Changed to state: {state_name}")

    def update_game_time(self):
        """Update in-game time based on real time passage"""
        elapsed_time = pygame.time.get_ticks() - self.start_ticks

        if elapsed_time >= 20000:  # 20 seconds = 1 hour in-game
            self.start_ticks = pygame.time.get_ticks()
            self.hour += 1

            if self.hour == 24:
                self.hour = 0
                self.day += 1

    def draw_clock(self):
        """Draw the in-game clock/calendar"""
        time_text = f"Day {self.day} | {self.hour:02}:00"
        time_surface = self.font.render(time_text, True, (255, 255, 255))
        # Draw in the top-right corner
        self.screen.blit(time_surface, (self.WIDTH - 150, 10))

    def get_exit_side(self, player_pos, center):
        """Determine which side of the diamond the player is exiting through"""
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

    def draw_inventory(self):
        """Draw the player's inventory UI"""
        for slot in range(self.player.inventory_cap):
            x = self.INVENTORY_SLOT_SIZE + (slot * self.INVENTORY_SLOT_SIZE)
            color = (150, 150, 150) if slot != self.player.selected_inventory_slot else (
                255, 255, 255)
            pygame.draw.rect(self.screen, color, (x, self.INVENTORY_Y,
                             self.INVENTORY_SLOT_SIZE, self.INVENTORY_SLOT_SIZE), 2)
            pygame.draw.rect(self.screen, (50, 50, 50), (x + 2, self.INVENTORY_Y + 2,
                             self.INVENTORY_SLOT_SIZE - 4, self.INVENTORY_SLOT_SIZE - 4))

            item, count = self.player.inventory[slot]
            if item:
                if isinstance(item, OxygenTank):
                    self.screen.blit(item.icon, (x + 5, self.INVENTORY_Y + 5))
                    oxygen_text = f"{int(item.oxygen)}/{item.oxygen_cap}"
                    text = self.font.render(oxygen_text, True, (255, 255, 255))
                    self.screen.blit(text, (x + 5, self.INVENTORY_Y + 20))
                elif item.icon:
                    self.screen.blit(item.icon, (x + 5, self.INVENTORY_Y + 5))
                if count > 1:
                    count_text = self.font.render(
                        str(count), True, (255, 255, 255))
                    self.screen.blit(
                        count_text, (x + 25, self.INVENTORY_Y + 25))

    def draw_stat_bar(self, icon, value, max_value, x, y, color):
        """Draw a stat bar with icon"""
        self.screen.blit(icon, (x - 25, y - 5))
        pygame.draw.rect(self.screen, (50, 50, 50),
                         (x, y, self.bar_width, self.bar_height))
        fill_width = (value / max_value) * self.bar_width
        pygame.draw.rect(self.screen, color,
                         (x, y, fill_width, self.bar_height))

    def update_stats(self, moving=False, tile_type="blank"):
        """Update player's stats based on time and conditions"""
        self.player.hunger = min(self.player.hunger - self.HUNGER_RATE, 100)
        self.player.thirst = max(self.player.thirst - self.THIRST_RATE, 0)
        self.player.oxygen = max(self.player.oxygen - self.OXYGEN_RATE, 0)

        # Health effects
        if self.player.oxygen <= 0:
            self.player.health = max(self.player.health - self.HEALTH_RATE, 0)

        if self.player.hunger >= 100 or self.player.thirst <= 0:
            self.player.health = max(self.player.health - self.HEALTH_RATE, 0)

    async def game_loop(self):
        """Main game loop"""
        running = True
        last_time = time.time()

        while running:
            # Calculate delta time
            current_time = time.time()
            dt = current_time - last_time
            last_time = current_time

            # Get events once per frame
            events = pygame.event.get()

            # Check for quit
            for event in events:
                if event.type == pygame.QUIT:
                    running = False

            # Let current state handle events
            self.current_state.handle_events(events)

            # Update current state
            self.current_state.update(dt)

            # Render current state
            self.current_state.render(events=events)

            # Update display
            pygame.display.flip()
            self.clock.tick(60)

            await asyncio.sleep(0.01)  # For asyncio compatibility

    async def main(self):
        """Game entry point"""
        await self.game_loop()


if __name__ == "__main__":
    game = Game()
    asyncio.run(game.main())
