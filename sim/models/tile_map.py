from sim.models import tile
from sim.models.terrain import Terrain
from sim.models.terrain_improvement import TerrainImprovement

class TileMapException(Exception):
	def __init__(self, message):
		self.message = message
	def __str__(self):
		return self.message

class TileMap:

	def __init__(self, x_min, y_min, x_max, y_max):
		if x_max <= x_min:
			raise TileMapException("x_max must be greater than x_min")
		(self.x_min, self.x_max) = (x_min, x_max)

		if y_max <= y_min:
			raise TileMapEyception("y_max must be greater than y_min")
		(self.y_min, self.y_max) = (y_min, y_max)

		self.tile_array = {}
		for x in range(x_min, x_max):
			for y in range(y_min, y_max):
				self.tile_array[x, y] = tile.Tile(x, y, Terrain)
				self.tile_array[x, y].terrain_improvement = TerrainImprovement

		self.building_registry = {}
		self.reverse_building_registry = {}
		self.unit_registry = {}

	def place_building(self, building, x, y):
		if not self.in_bounds(x, y):
			raise TileMapException("Buildings must be placed in bounds")
		if self.get_building_at_position(x, y) is not None:
			raise TileMapException("There is already a building at that position")
		self.building_registry[building.building_id] = {
			'building' : building,
			'position' : (x, y),
			}
		self.reverse_building_registry[x, y] = building

	def place_unit(self, unit, x, y):
		if not self.in_bounds(x, y):
			raise TileMapException("Units must be placed in bounds")
		self.unit_registry[unit.unit_id] = {
			'unit'     : unit,
			'position' : (x, y),
			}
		unit.set_tile_map(self)

	def get_units(self):
		return [ v['unit'] for v in self.unit_registry.values() ]

	def move_unit(self, unit, dx, dy):
		# TODO: add error checks
		(x, y) = self.get_unit_position(unit)
		self.set_unit_position(unit, x + dx, y + dy)

	def get_unit_position(self, unit):
		if unit.unit_id not in self.unit_registry:
			raise TileMapException("That unit has not been added to the tile map: {}".format(unit))
		return self.unit_registry[unit.unit_id]['position']

	def set_unit_position(self, unit, x, y):
		if unit.unit_id not in self.unit_registry:
			raise TileMapException("That unit has not been added to the tile map: {}".format(unit))
		self.unit_registry[unit.unit_id]['position'] = (x, y)

	def get_building_position(self, building):
		if building.building_id not in self.building_registry:
			raise TileMapException("That building has not been added to the tile map: {}".format(building))
		return self.building_registry[building.building_id]['position']

	def get_building_at_position(self, x, y):
		return self.reverse_building_registry.get((x, y))

	def set_terrain(self, terrain, x, y):
		if not self.in_bounds(x, y):
			raise TileMapException("out of bounds!")
		self.tile_array[x, y].terrain_type = terrain

	def get_terrain(self, x, y):
		if not self.in_bounds(x, y):
			raise TileMapException("out of bounds!")
		return self.tile_array[x, y].terrain_type

	def get_terrain_under_unit(self, unit):
		if unit.unit_id not in self.unit_registry:
			raise TileMapException("That unit has not been added to the tile map: {}".format(unit))
		(x, y) = self.get_unit_position(unit)
		return self.get_terrain(x, y)

	def set_terrain_improvement(self, improvement, x, y):
		if not self.in_bounds(x, y):
			raise TileMapException("out of bounds!")
		self.tile_array[x, y].terrain_improvement = improvement

	def get_terrain_improvement(self, x, y):
		if not self.in_bounds(x, y):
			raise TileMapException("out of bounds!")
		return self.tile_array[x, y].terrain_improvement

	def get_tile(self, x, y):
		if not self.in_bounds(x, y):
			raise TileMapException("out of bounds!")
		return self.tile_array[x, y]

	def in_bounds(self, x, y):
		if x in range(self.x_min, self.x_max) and y in range(self.y_min, self.y_max):
			return True
		else:
			return False
