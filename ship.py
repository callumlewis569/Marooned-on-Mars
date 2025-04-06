class Ship():
    def __init__(self, oxygen, oxygen_cap, fuel, fuel_cap):
        self.oxygen = oxygen
        self.oxygen_cap = oxygen_cap
        self.fuel = fuel
        self.fuel_cap = fuel_cap 

    def add_fuel(self, fuel):
        self.fuel = min(self.fuel+fuel,self.fuel_cap)

    def add_oxygen(self, oxygen):
        self.oxygen = min(self.oxygen+oxygen,self.oxygen_cap)

    def ship_running(self, game_runnng):
        if (game_runnng):
            self.fuel -= 1
            self.oxygen -= 1
    