import pygame
import sys
from character import Character

# Initialisation
pygame.init()
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Marooned on Mars")

clock = pygame.time.Clock()

# Load images
background = pygame.image.load("assets/tile_2.png")


# Display text
pygame.font.init()
my_font = pygame.font.SysFont('Times New Roman', 15)
# text_surface = my_font.render(f'Food: {food}', False, (255, 255, 255))
# text_surface = my_font.render(f'Water: {water}', False, (255, 255, 255))
# text_surface = my_font.render(f'Fuel: {fuel}', False, (255, 255, 255))
# text_surface = my_font.render(f'Oxygen: {oxygen}', False, (255, 255, 255))

# Set initial player position
player_x = WIDTH / 2
player_y = HEIGHT / 2
player_speed = 1
player_hunger = 0
player_fuel = 100
player_oxygen = 100
player_health = 100

player = Character(
    player_x, 
    player_y, 
    player_speed, 
    player_hunger, 
    player_fuel, 
    player_oxygen, 
    player_health
)


# Game Loop
running = True
while running:
    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Key Press Handling
    player.move()

    # Drawing
    screen.fill(0)
    screen.blit(background, (0, 0))
    screen.blit(player.image, (player.x, player.y))
    # screen.blit(text_surface, (0,0))

    pygame.display.flip()
    clock.tick(60)
