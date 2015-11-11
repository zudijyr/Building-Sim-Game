from sim import SimException
from sim.models import tile
from sim.models.terrain import Terrain
from sim.models.terrain_improvement import TerrainImprovement

class TileMapException(SimException): pass

class TileMap:

	def __init__(self, tile_grid, tile_w):
		"""
		TODO: Have the tile_map build it's own tile grid and init tile_map
			  with a w, h of the map that is then subdivided into tiles on
			  the tile grid.
			  Decide what to do about w, h that falls within a tile instead
			  of on the boundary
		"""
		if tile_w <= 0:
			raise TileMapException("Tile width must be positive")
		self.tile_w = tile_w
		(self.w, self.h) = (tile_grid.w * tile_w, tile_grid.h * tile_w)
		self.tile_grid = tile_grid

		self.building_registry = {}
		self.reverse_building_registry = {}
		self.unit_registry = {}

	def place_building_on_grid(self, building, grid_x, grid_y):
		(map_x, map_y) = self.grid_coords_to_map_coords(grid_x, grid_y)
		(map_x, map_y) = (map_x + 0.5 * self.tile_w, map_y + 0.5 * self.tile_w)
		self.place_building(building, map_x, map_y)

	def place_building(self, building, x, y):
		if not self.in_bounds(x, y):
			raise TileMapException("Buildings must be placed in bounds")
		# TODO: Compute building overlaps here
		#if self.get_building_at_position(x, y) is not None:
		#    raise TileMapException("There is already a building at that position")
		self.building_registry[building.building_id] = {
			'building' : building,
			'position' : (x, y),
			}
		self.reverse_building_registry[x, y] = building

	def place_unit_on_grid(self, building, grid_x, grid_y):
		(map_x, map_y) = self.grid_coords_to_map_coords(grid_x, grid_y)
		(map_x, map_y) = (map_x + 0.5 * self.tile_w, map_y + 0.5 * self.tile_w)
		self.place_unit(building, map_x, map_y)

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

	def get_buildings(self):
		# TODO: test me
		return [ v['building'] for v in self.building_registry.values() ]

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

	# This will need look for building overlapping the coordinates
	#def get_building_at_position(self, x, y):
	#    return self.reverse_building_registry.get((x, y))

	def get_tile_under_unit(self, unit):
		if unit.unit_id not in self.unit_registry:
			raise TileMapException("That unit has not been added to the tile map: {}".format(unit))
		(x, y) = self.get_unit_position(unit)
		return self.get_tile(x, y)

	def get_tile(self, x, y):
		if not self.in_bounds(x, y):
			raise TileMapException("out of bounds: ({}, {})".format(x, y))
		return self.tile_grid.get_tile(*self.map_coords_to_grid_coords(x, y))

	def map_coords_to_grid_coords(self, map_x, map_y):
		return (map_x // self.tile_w, map_y // self.tile_w)

	def grid_coords_to_map_coords(self, tile_x, tile_y):
		return (tile_x * self.tile_w, tile_y * self.tile_w)

	def in_bounds(self, x, y):
		if x >= 0 and x < self.w and y >= 0 and y < self.h:
			return True
		else:
			return False
