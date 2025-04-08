#Item File used to create Item classes aswell as Initiate the items at the end.
import pygame
#Parent Item class defines item name and weight
class Item():
    def __init__(self, item_name, item_weight):
        self.name = item_name
        self.weight = item_weight
#Inherited Fuel class further defines the type, energy and mining level
class Fuel(Item):
    def __init__(self, item_name, item_weight, energy, mining_lvl):
        super().__init__(item_name, item_weight)
        self.type = "Fuel"
        self.energy = energy
        self.mining_lvl = mining_lvl
#Inherited Ore class further defines the type and mining level
class Ore(Item):
    def __init__(self, item_name, item_weight, mining_lvl):
        super().__init__(item_name, item_weight)
        self.type = "Ore"
        self.mining_lvl = mining_lvl
#Inherited Radioactive class further defines the type, rads and mining level
class Radioactive(Item):
    def __init__(self, item_name, item_weight, rad, mining_lvl):
        super().__init__(item_name, item_weight)
        self.type = "Radioactive"
        self.rad = rad
        self.mining_lvl = mining_lvl
#Inherited Plant class further defines the type, satiation, oxygen potential and mining level
class Plant(Item):
    def __init__(self, item_name, item_weight, satiation, oxypot, grow_rate, icon=None):
        super().__init__(item_name, item_weight)
        self.type = "Plant"
        self.satiation = satiation
        self.oxypot = oxypot
        self.grow_rate= grow_rate
        self.icon = icon # Ahmed a added this to make sure the photos show in the inventory
#Inherited Oxygen Tank class further defines the oxygen levels and cap      
class OxygenTank(Item):
    def __init__(self, item_name, item_weight, oxygen_cap, oxygen=0):
        super().__init__(item_name,item_weight)
        self.oxygen_cap = oxygen_cap  # Fixed capacity (e.g., 100)
        self.oxygen = oxygen          # Current oxygen level
    #Function used to add Oxygen to the tanks
    def add_oxygen(self, amount):
        self.oxygen = min(self.oxygen + amount, self.oxygen_cap)
        print(f"Adding {amount} to tank, Oxygen: {self.oxygen}, Capacity: {self.oxygen_cap}")
    #Function to upgrade the tank
    def upgrade_tank(self, oxygen_cap):
        self.oxygen_cap = oxygen_cap
        self.oxygen = oxygen_cap
#Drillbit class defines the name and drill bit level (Mining power)
class DrillBit():
    def __init__(self, name, drill_bit):
        self.name = name
        self.drill_bit = drill_bit
#Battery class defines the name and battery level (How much power the drill has before it need to recharge)
class Battery():
    def __init__(self, name, battery):
        self.name = name
        self.battery = battery
#Drill class defines the name, battery and drill bit (could also potentially use this to setup automated mines too??)
class Drill():
    def __init__(self, battery, drill_bit):
        self.name = "Drill"
        self.battery = battery
        self.battery_cap = battery
        self.drill_bit = drill_bit
        self.drill_running = False
    #Function to allow users to rename their drills
    def update_name(self, name):
        self.name = name
    #Function to upgrade drillbit
    def upgrade_drill_bit(self, drill_bit):
        self.drill_bit = drill_bit
    #Function to upgrade battery
    def upgrade_battery(self, battery):
        self.battery = battery
        self.battery_cap = battery
    #Funtion to charde the drill
    def charge_drill(self, battery):
        self.battery = min(self.battery + battery, self.battery_cap)
    #Function to start the drill
    def drill_run(self):
        self.drill_running = True
        while (self.drill_running):
            self.battery -= 1
            if (self.battery == 0):
                self.drill_running = False
    #Function to stop the drill
    def drill_stop(self):
        self.drill_running = False


# Initialisation of Items:
fuels = {
    "Combustite": Fuel("Combustite", 1, 30, 1),
    "Ionflux": Fuel("Ionflux", 1.5, 60, 4),
    "Void Ether": Fuel("Void Ether", 2, 90, 7)
}

ores = {
    "Rustalon": Ore("Rustalon", 1, 1),
    "Hexacron": Ore("Hexacron", 1.5, 4),
    "Xerocite": Ore("Xerocite", 2, 7)
}

radioactives = {
    "Nytrazine": Radioactive("Nytrazine", 1, 1, 1),
    "Tatonium": Radioactive("Tatonium", 1.5, 4, 4),
    "Aetherium-94": Radioactive("Aetherium-94", 2, 6, 7)
}

plants = {
    "Basic Potato": Plant("Basic Potato", 0.5, 20, 5, 30, icon= pygame.transform.scale(
    pygame.image.load("assets/basic_potato.png"), (30, 30))),
    "Mars Potato": Plant("Mars Potato", 1, 30, 5, 60, pygame.transform.scale(
    pygame.image.load("assets/mars_potato.png"), (30, 30)
)),
    "Tree Potato": Plant("Tree Potato", 1, 0, 10, 60, icon=pygame.transform.scale(
    pygame.image.load("assets/tree_potato.png"), (30, 30)
))
}

oxygen_tanks = {
    "Oxygen Tank A": OxygenTank("Oxygen Tank A",1,100),
    "Oxygen Tank B": OxygenTank("Oxygen Tank B",1,100)
}

drill_bits = [
    DrillBit("Rustalon Drill Bit 1", 1),
    DrillBit("Rustalon Drill Bit 2", 2),
    DrillBit("Rustalon Drill Bit 3", 3),
    DrillBit("Hexacron Drill Bit 1", 4),
    DrillBit("Hexacron Drill Bit 2", 5),
    DrillBit("Hexacron Drill Bit 3", 6),
    DrillBit("Xerocite Drill Bit 1", 7),
    DrillBit("Xerocite Drill Bit 2", 8),
    DrillBit("Xerocite Drill Bit 3", 9)
]

batteries = [
    Battery("Potato Battery", 50),
    Battery("Spark Unit", 100),
    Battery("Pulse Pak", 200),
    Battery("Void Crystal", 300)
]

player_drill = Drill(batteries[0].battery, drill_bits[0].drill_bit)
        

        
