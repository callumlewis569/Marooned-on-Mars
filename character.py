import pygame
from item import *
from Interactions import PlacedOxygenTank
class Character():
    def __init__(self, x, y, map_x, map_y, speed, hunger, thirst, fuel, oxygen, health):
        self.image = pygame.image.load("assets/character.png")
        self.x = x
        self.y = y
        self.map_x = map_x
        self.map_y = map_y
        self.speed = speed
        self.hunger = hunger
        self.hunger_cap = 100 
        self.thirst = thirst
        self.thirst_cap = 100 
        self.fuel = fuel
        self.fuel_cap = 100 
        self.oxygen = oxygen
        self.oxygen_cap = 100 
        self.health = health
        self.health_cap = 100
        self.inventory = {}
        self.inventory_cap = 10
        self.hotbar = [(None, 0)] * 9
        self.selected_hotbar_slot = 0  # Currently selected slot (0-8)

    def move(self, map_width, map_height):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed

        if self.x < 0:
            self.x = 0
        elif self.x + 16 > map_width:
            self.x = map_width - 16

        if self.y < 0:
            self.y = 0
        elif self.y + 16 > map_height:
            self.y = map_height - 16

    def add_ox(self, oxygen):
        self.oxygen = min(self.oxygen + oxygen, self.oxygen_cap)

    def add_item(self, item):
        # Handle OxygenTank separately
        if isinstance(item, OxygenTank) or isinstance(item, PlacedOxygenTank):
            for i in range(len(self.hotbar)):
                if self.hotbar[i][0] is None:
                    self.hotbar[i] = (item, 1)  # Add the specific tank instance
                    return True
            return False

        # Original stacking logic for other items
        for i in range(len(self.hotbar)):
            current_item, count = self.hotbar[i]
            if current_item and current_item.name == item.name:
                self.hotbar[i] = (current_item, count + 1)
                return True
            elif current_item is None:
                self.hotbar[i] = (item, 1)
                return True

        inventory_size = sum(self.inventory.get(i, 0) for i in self.inventory)
        if inventory_size < self.inventory_cap:
            self.inventory[item.name] = self.inventory.get(item.name, 0) + 1
            return True
        return False
    def remove_item(self, slot):
        # Decrease count in selected slot, remove if count reaches 0
        item, count = self.hotbar[slot]
        if item and count > 0:
            count -= 1
            if count == 0:
                self.hotbar[slot] = (None, 0)
            else:
                self.hotbar[slot] = (item, count)
            return True
        return False

    def select_hotbar(self, slot):
        if 0 <= slot <= 8:
            self.selected_hotbar_slot = slot