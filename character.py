import pygame
from item import *
from interactions import PlacedOxygenTank

class Character:
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
        self.inventory = {i: (None, 0) for i in range(10)}
        self.inventory_cap = 10
        self.selected_inventory_slot = 0

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

    def inc_item(self, item):
        try:
            self.inventory[item] += 1
        except KeyError:
            self.inventory[item] = 1

    def add_ox(self, oxygen):
        self.oxygen = min(self.oxygen + oxygen, self.oxygen_cap)

    def add_item(self, item, count=1):
        # Stack item if it already exists in a slot
        for i in range(self.inventory_cap):
            current_item, current_count = self.inventory[i]
            if current_item and current_item.name == item.name:
                self.inventory[i] = (current_item, current_count + count)
                return True

        # Otherwise find empty slot
        for i in range(self.inventory_cap):
            current_item, _ = self.inventory[i]
            if current_item is None:
                self.inventory[i] = (item, count)
                return True

        return False  # Inventory full

    # def remove_item(self, slot):
    #     """Remove an item from the specified hotbar slot."""
    #     if not (0 <= slot < len(self.hotbar)):
    #         return False  # Invalid slot
    #
    #     item, count = self.hotbar[slot]
    #     if item and count > 0:
    #         count -= 1
    #         if count == 0:
    #             self.hotbar[slot] = (None, 0)  # Clear the slot if count reaches 0
    #         else:
    #             self.hotbar[slot] = (item, count)  # Update with reduced count
    #         return True
    #     return False  # No item to remove

    def select_inventory(self, slot):
        if 0 <= slot <= 8:
            self.selected_inventory_slot = slot
            return self.inventory[slot]
        return None
