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

class KeyBinds:
    def __init__(self, game):
        self.game = game

    def pressing_p(self, selected_slot, item, count):
        if count >= 1:
            if isinstance(item, Plant):
                # Place the plant in the world
                placed = PlacedPlant(self.game.player.x, self.game.player.y, self.game.player.map_x,
                                     self.game.player.map_y, item, self.game)
                self.game.planted_crops.append(placed)

                # Decrease item count
                if count == 1:
                    self.game.player.inventory[selected_slot] = (None, 0)
                else:
                    self.game.player.inventory[selected_slot] = (item, count - 1)
                print(f"Planted {item.name} at ({self.game.player.x}, {self.game.player.y})")

            if isinstance(item, OxygenTank):
                placed = PlacedOxygenTank(self.game.player.x, self.game.player.y, self.game.player.map_x,
                                          self.game.player.map_y, item, self.game, self.game.player)
                self.game.oxygen_tanks.append(placed)
                # Decrease item count
                if count == 1:
                    self.game.player.inventory[selected_slot] = (None, 0)
                else:
                    self.game.player.inventory[selected_slot] = (item, count - 1)
                print(f"Planted {item.name} at ({self.game.player.x}, {self.game.player.y})")

    def pressing_u(self, selected_slot, item, count):
        if isinstance(item, OxygenTank):
            for tank in self.game.player.transferring_tanks[:]:
                if tank.oxygen > 0:
                    tank.transfer_oxygen(self.game.player)
        elif isinstance(item, Plant):
            if count > 0 and self.game.player.hunger != self.game.player.hunger_cap:
                item.eat(self.game.player, selected_slot)
            else:
                print("You are already full! You can't eat more.")

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
