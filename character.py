import pygame

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
        for i in self.inventory:
            inventory_size += self.inventory.get(i)

        if (inventory_size < self.inventory_cap):
            if (item in self.inventory.items):
                self.inventory[item] += 1
            else:
                self.inventory[item] = 1
        elif (inventory_size >= self.inventory_cap):
            inventory_full = True
            return inventory_full
