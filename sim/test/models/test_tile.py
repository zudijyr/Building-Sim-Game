import unittest
from sim.models.tile import *
from sim.models.terrain import *
from sim.models.terrain_improvement import *

class TileModelTest(unittest.TestCase):

    def test_tile_starts_with_default_improvement(self):
        tile1 = Tile(1,2, terrain.Grass)
        assert(tile1.terrain_type.move_cost == terrain.Grass.move_cost)
        assert(tile1.terrain_improvement  == terrain_improvement.TerrainImprovement)
