class Ship():
    def __init__(self, oxygen, fuel):
        self.oxygen = oxygen
        self.fuel = fuel 

    def add_fuel(self, fuel):
        self.fuel += fuel

    def add_oxygen(self, oxygen):
        self.oxygen += oxygen

    def ship_running(self, game_runnng):
        if (game_runnng):
            self.fuel -= 1
            self.oxygen -= 1
    