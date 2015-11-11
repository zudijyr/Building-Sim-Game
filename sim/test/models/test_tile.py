import unittest
from sim.models.tile import Tile
from sim.models.terrain import Grass
from sim.models.terrain_improvement import TerrainImprovement

class TileModelTest(unittest.TestCase):

	def test_set_terrain_sets_the_terrain_for_a_tile(self):
		tile = Tile()
		tile.set_terrain(Grass)
		self.assertIs(tile.terrain, Grass)
		self.assertIs(tile.terrain_improvement, TerrainImprovement)
