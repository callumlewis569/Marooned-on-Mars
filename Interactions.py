from item import Plant, OxygenTank, plants, oxygen_tanks
import time
import pygame
import math
class PlacedOxygenTank:
    def __init__(self, x, y, map_x, map_y ,oxygentank: OxygenTank,  game, player):
        self.x = x
        self.y = y
        self.map_x = map_x
        self.map_y = map_y
        self.oxygentank = oxygentank
        self.game = game
        self.player = player

    def draw(self, screen, font):
        icon = self.oxygentank.icon
        screen.blit(icon, (self.x, self.y))
        oxygen_text = f"{int(self.oxygentank.oxygen)}/{self.oxygentank.oxygen_cap} O2"
        text = font.render(oxygen_text, True, (255, 255, 255))
        screen.blit(text, (self.x, self.y - 20))

    def check_near_plant(self):
        for plant in self.game.planted_crops:
            distance = math.hypot(self.x - plant.x, self.y - plant.y)
            if distance < 40:
                self.oxygentank.oxygen = min(
                    self.oxygentank.oxygen + plant.plant.oxypot * 0.1,
                    self.oxygentank.oxygen_cap
                )
    def pickup(self):

        picked_up_tank = OxygenTank(
            self.oxygentank.name,
            self.oxygentank.weight,
            self.oxygentank.oxygen_cap,
            self.oxygentank.oxygen,
            self.oxygentank.icon
        )
        return picked_up_tank



class PlacedPlant:
    def __init__(self, x, y, map_x, map_y ,plant: Plant, game):
        self.x = x
        self.y = y
        self.map_x = map_x
        self.map_y = map_y
        self.plant = plant
        self.plant_time = time.time()
        self.ready = False
        self.game = game

    def check_harvest(self):
        elapsed = time.time() - self.plant_time
        if elapsed >= self.plant.grow_rate:
            self.ready = True

    def get_growth_progress(self):
        distance = math.hypot(self.x - self.game.player.x, self.y - self.game.player.y)
        if distance < 40:
            self.game.player.oxygen = min(
                self.game.player.oxygen + self.plant.oxypot * 0.01,
                self.game.player.oxygen_cap
            )

        elapsed = time.time() - self.plant_time
        return min(elapsed / self.plant.grow_rate, 1.0)  # capped at 1.0

    def draw(self, screen):
        icon = self.plant.icon
        screen.blit(icon, (self.x, self.y))
        # Draw growth bar above the plant
        bar_width = 30
        bar_height = 5
        bar_x = self.x
        bar_y = self.y - 8  # position bar slightly above the plant
        progress = self.get_growth_progress()
        pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 200, 0), (bar_x, bar_y, bar_width * progress, bar_height))

    def harvest(self):
        if not self.ready:
            return []
        self.ready = False
        harvest_yields = {
            "Basic Potato": 2,
            "Mars Potato": 4,
            "Tree Potato": 1
        }
        count = harvest_yields.get(self.plant.name, 1)  # Default to 1 if not found
        harvested_plants = [plants[self.plant.name] for _ in range(count)]
        return harvested_plants

