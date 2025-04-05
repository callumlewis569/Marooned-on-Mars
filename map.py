class Map():
    def __init__(self, size, seed):
        self.map = [[None for i in range(size)] for i in range(size)]

map = Map(10, 0)
print(map.map)