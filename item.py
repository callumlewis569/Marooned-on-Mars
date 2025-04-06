class Item():
    def __init__(self, item_name, item_weight):
        self.name = item_name
        self.weight = item_weight

class Fuel(Item):
    def __init__(self, item_name, item_weight, energy, mining_lvl):
        super().__init__(item_name, item_weight)
        self.energy = energy
        self.mining_lvl = mining_lvl

class Ore(Item):
    def __init__(self, item_name, item_weight, mining_lvl):
        super().__init__(item_name, item_weight)
        self.type = "Ore"
        self.mining_lvl = mining_lvl

class Radioactive(Item):
    def __init__(self, item_name, item_weight, rad, mining_lvl):
        super().__init__(item_name, item_weight)
        self.type = "Radioactive"
        self.rad = rad
        self.mining_lvl = mining_lvl

class Plant(Item):
    def __init__(self, item_name, item_weight, satiation, oxypot, grow_rate):
        super().__init__(item_name, item_weight)
        self.type = "Plant"
        self.satiation = satiation
        self.oxypot = oxypot
        self.grow_rate= grow_rate
        
class OxygenTank:
    def __init__(self, item_name, item_weight, oxygen_cap, oxygen=0):
        self.item_name = item_name
        self.item_weight = item_weight
        self.oxygen_cap = oxygen_cap  # Fixed capacity (e.g., 100)
        self.oxygen = oxygen          # Current oxygen level

    def add_oxygen(self, amount):
        self.oxygen = min(self.oxygen + amount, self.oxygen_cap)
        print(f"Adding {amount} to tank, Oxygen: {self.oxygen}, Capacity: {self.oxygen_cap}")
    def upgrade_tank(self, oxygen_cap):
        self.oxygen_cap = oxygen_cap
        self.oxygen = oxygen_cap

class DrillBit():
    def __init__(self, name, drill_bit):
        self.name = name
        self.drill_bit = drill_bit

class Battery():
    def __init__(self, name, battery):
        self.name = name
        self.battery = battery

class Drill():
    def __init__(self, battery, drill_bit):
        self.name = "Drill"
        self.battery = battery
        self.battery_cap = battery
        self.drill_bit = drill_bit
        self.drill_running = False

    def update_name(self, name):
        self.name = name

    def update_drill_bit(self, drill_bit):
        self.drill_bit = drill_bit

    def update_battery(self, battery):
        self.battery = battery
        self.battery_cap = battery

    def charge_drill(self, battery):
        self.battery = min(self.battery + battery, self.battery_cap)

    def drill_run(self):
        self.drill_running = True
        while (self.drill_running):
            self.battery -= 1
            if (self.battery == 0):
                self.drill_running = False
    
    def drill_stop(self):
        self.drill_running = False


        
