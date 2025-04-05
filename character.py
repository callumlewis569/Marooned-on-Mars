import pygame

class Character():
    def __init__(self, x, y, speed, hunger, fuel, oxygen, health):
        self.image = pygame.image.load("assets/character.png")
        self.x = x
        self.y = y
        self.speed = speed
        self.hunger = hunger
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