from sim.models import terrain
from sim.models import tile
from sim.models.terrain_improvement import *

class TileMap:

	def __init__(self, x_min, y_min, x_max, y_max):
		assert x_max > x_min
		(self.x_min, self.x_max) = (x_min, x_max)

		assert y_max > y_min
		(self.y_min, self.y_max) = (y_min, y_max)

		self.tile_array = {}
		for x in range(x_min, x_max):
			for y in range(y_min, y_max):
				self.tile_array[x, y] = tile.Tile(x,y,terrain.Terrain)
				self.tile_array[x, y].terrain_improvement = TerrainImprovement

		self.building_registry = {}
		self.unit_registry = {}

	def place_building(self, building, x, y):
		self.building_registry[building.building_id] = (x, y)

	def place_unit(self, unit, x, y):
		# TODO: add error checks
		self.unit_registry[unit.unit_id] = (x, y)
		unit.set_tile_map(self)

	def move_unit(self, unit, dx, dy):
		# TODO: add error checks
		(x, y) = self.get_unit_position(unit)
		self.unit_registry[unit.unit_id] = (x + dx, y + dy)

	def get_unit_position(self, unit):
		if unit.unit_id not in self.unit_registry:
			raise TileMapException("That unit has not been added to the tile map: {}".format(unit))
		return self.unit_registry[unit.unit_id]

	def set_terrain(self, terrain, x, y):
		assert x >= self.x_min and x < self.x_max
		assert y >= self.y_min and y < self.y_max
		self.tile_array[x, y].terrain_type = terrain

	def get_terrain(self, x, y):
		assert x >= self.x_min and x < self.x_max
		assert y >= self.y_min and y < self.y_max
		return self.tile_array[x, y].terrain_type

	def get_terrain_under_unit(self, unit):
		if unit.unit_id not in self.unit_registry:
			raise TileMapException("That unit has not been added to the tile map: {}".format(unit))
		(x, y) = self.get_unit_position(unit)
		return self.get_terrain(x, y)

	def set_terrain_improvement(self, improvement, x, y):
		assert x >= self.x_min and x < self.x_max
		assert y >= self.y_min and y < self.y_max
		self.tile_array[x, y].terrain_improvement = improvement

	def get_terrain_improvement(self, x, y):
		assert x >= self.x_min and x < self.x_max
		assert y >= self.y_min and y < self.y_max
		return self.tile_array[x, y].terrain_improvement

	def get_tile(self, x, y):
		assert x >= self.x_min and x < self.x_max
		assert y >= self.y_min and y < self.y_max
		return self.tile_array[x, y]

	def in_bounds(self, new_x, new_y):
		# TODO: Consider using ranges here
		if new_x < self.x_min:
				return False
		elif new_y < self.y_min:
				return False
		elif new_x >= self.x_max:
				return False
		elif new_x >= self.y_max:
				return False
		else:
			return True
