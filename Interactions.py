from item import Plant, OxygenTank
import time
import pygame

class PlacedOxygenTank(OxygenTank):
    def __init__(self, x, y, map_x, map_y, item_name, item_weight, oxygen_cap, oxygen=0):
        super().__init__(item_name, item_weight, oxygen, oxygen_cap)
        self.x = x
        self.y = y
        self.map_x = map_x  # Add map coordinates
        self.map_y = map_y  # Add map coordinates
        self.image = pygame.image.load("assets/oxygen.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))

    def draw(self, screen, font):
        oxygen_text = f"{int(self.oxygen)}/{self.oxygen_cap} O2"
        text = font.render(oxygen_text, True, (255, 255, 255))
        screen.blit(self.image, (self.x, self.y))
        screen.blit(text, (self.x, self.y - 20))
class FarmPlot:
    def __init__(self, x, y, map_x, map_y):
        self.x = x
        self.y = y
        self.map_x = map_x
        self.map_y = map_y
        self.planted_item = None
        self.plant_time = 0
        self.ready = False

    def plant(self, item):
        if isinstance(item, Plant) and not self.planted_item:
            self.planted_item = item
            self.plant_time = time.time()
            self.ready = False
            return True
        return False

    def check_harvest(self):
        if self.planted_item and time.time() - self.plant_time >= self.planted_item.grow_rate:
            self.ready = True
            return True
        return False

    def harvest(self):
        if self.ready:
            item = self.planted_item
            self.planted_item = None
            self.ready = False
            return [Plant(item.name, item.weight, item.satiation, item.oxypot, item.grow_rate) for _ in range(3)]
        return None

    def get_growth_progress(self):
        if self.planted_item:
            elapsed_time = time.time() - self.plant_time
            progress = min(elapsed_time / self.planted_item.grow_rate, 1)
            return progress
        return 0

