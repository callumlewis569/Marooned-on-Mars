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
        self.thirst = thirst
        self.fuel = fuel
        self.oxygen = oxygen
        self.health = health

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed