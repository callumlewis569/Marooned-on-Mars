import random
import math

class Map():
    def __init__(self, size, seed):
        # Initialise empty grid
        self.map = [[None for i in range(size)] for i in range(size)]

        random.seed(seed)

        center_x, center_y = size // 2, size // 2

        def distance_to_center(x, y):
            return math.hypot(x - center_x, y - center_y)

        def distance_to_edge(x, y):
            return min(x, y, size - 1 - x, size - 1 - y)

        max_center_dist = distance_to_center(0, 0)
        max_edge_dist = min(center_x, center_y)

        for y in range(size):
            for x in range(size):
                d_center = distance_to_center(x, y) / max_center_dist
                d_edge = distance_to_edge(x, y) / max_edge_dist

                # Determine tile based on rules
                roll = random.random()

                if d_edge < 0.4:
                    if roll < 0.7:
                        tile = 'mountain'
                    elif roll < 0.8:
                        tile = 'cave'
                    else:
                        tile = 'blank'
                elif 0.4 < d_center < 0.7:
                    if roll < 0.3:
                        tile = 'ore'
                    else:
                        tile = 'blank'
                else:
                    tile = 'blank'

                self.map[y][x] = tile

    def get_tile(self, map_x, map_y):
        return self.map[map_x][map_y]

    def print_map(self):
        for row in self.map:
            print(' '.join(row))

if __name__ == "__main__":
    map = Map(10, 0)
    map.print_map()
