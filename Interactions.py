from item import Plant
import time

# class Interactions():
#     def __init__(self):
#         pass
#
#     def Mining():
#         pass


class FarmPlot:
    def __init__(self, x, y, map_x, map_y):
        self.x = x
        self.y = y
        self.map_x = map_x
        self.map_y = map_y
        self.planted_item = None
        self.plant_time = 0
        self.ready = False

    def plant(self, item):
        if self.planted_item is None and isinstance(item, Plant):
            self.planted_item = item
            self.plant_time = time.time()
            self.ready = False
            return True
        return False

    def check_harvest(self):
        if self.planted_item and not self.ready:
            if time.time() - self.plant_time >= self.planted_item.grow_rate:
                self.ready = True
        return self.ready

    def harvest(self):
        if self.ready:
            item = self.planted_item
            self.planted_item = None
            self.ready = False
            return item
        return None

