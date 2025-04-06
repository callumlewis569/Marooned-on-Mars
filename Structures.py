class Mines():
    def __init__(self, ore_name, mining_lvl):
        self.ore = ore_name
        self.mining_lvl = mining_lvl

    def Check_mine(self, drill_bit):
        if (drill_bit >= self.mining_lvl):
            self.mining_speed = 1 + (0.25 * (drill_bit - self.mining_lvl))
            mining = True
            return mining
        else:
            mining = False
            return mining
        
class Farm():
    def __init__(self, plant_name, oxypot, grow_rate):
        self.plant = plant_name
        self.oxypot = oxypot
        self.grow_rate = grow_rate
