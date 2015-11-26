from sim.models.terrain import Terrain
from sim.models.terrain_improvement import TerrainImprovement


class Tile:

	def __init__(self, tile_id=''):
		# The tile_id is currently only used for testing
		self.terrain = Terrain
		self.terrain_improvement = TerrainImprovement
		self.tile_id = tile_id

	def set_terrain(self, terrain):
		self.terrain = terrain

	def set_terrain_improvement(self, terrain_improvement):
		self.terrain_improvement = terrain_improvement
