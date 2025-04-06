class Ship():
    def __init__(self, oxygen, fuel, fuel_cap):
        self.oxygen = oxygen
        self.fuel = fuel
        self.fuel_cap = fuel_cap 

    def add_fuel(self, fuel):
        self.fuel = min(self.fuel+fuel,self.fuel_cap)

    def add_oxygen(self, oxygen):
        self.oxygen += oxygen

    def ship_running(self, game_runnng):
        if (game_runnng):
            self.fuel -= 1
            self.oxygen -= 1
    