from . import terrain
from . import terrain_improvement

class Tile:

    def __init__(self, x_position, y_position, terrain_type):
        self.x_position = x_position
        self.y_position = y_position
        self.terrain_type = terrain_type
        self.terrain_improvement = terrain_improvement.TerrainImprovement

    def displayTile(self):
        print('terrain_type : ', self.terrain_type, 'x_position : ', self.x_position, 'y_position : ', self.y_position)
