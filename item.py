class Item():
    def __init__(self, ID, item_name, item_weight):
        self.id = id
        self.name = item_name
        self.weight = item_weight

class Ore(Item):
    def __init__(self, ID, item_name, item_weight):
        super().__init__(ID, item_name, item_weight)
        self.type = "Ore"

class Radioactive(Item):
    def __init__(self, ID, item_name, item_weight, rad):
        super().__init__(ID, item_name, item_weight)
        self.type = "Radio"
        self.rad = rad

class Plant(Item):
    def __init__(self, ID, item_name, item_weight, satiation, oxypot):
        super().__init__(ID, item_name, item_weight)
        self.type = "Plant"
        self.satiation = satiation
        self.oxypot = oxypot
        
