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
