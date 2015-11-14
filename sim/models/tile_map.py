from sim import SimException
from sim.geometry import Point, Size, Vector, Rectangle
from sim.models import tile
from sim.models.terrain import Terrain
from sim.models.terrain_improvement import TerrainImprovement

class TileMapException(SimException): pass

class TileMap:

	def __init__(self, tile_grid, tile_sz=Size(20, 20)):
		"""
		TODO: Have the tile_map build it's own tile grid and init tile_map
			  with a w, h of the map that is then subdivided into tiles on
			  the tile grid.
			  Decide what to do about w, h that falls within a tile instead
			  of on the boundary
		"""
		if tile_sz.w <= 0.0 or tile_sz.h <= 0.0:
			raise TileMapException("The tile size must have positive area")
		self.tile_sz = tile_sz
		self.tile_grid = tile_grid
		map_sz = self.tile_grid.sz * tile_sz
		self.bounds_rect = Rectangle(Point(0, 0), map_sz)
		self.building_registry = {}
		self.unit_registry = {}
		self.selected_unit = None

	@property
	def w(self):
		return self.bounds_rect.w

	@property
	def h(self):
		return self.bounds_rect.h

	@property
	def sz(self):
		return self.bounds_rect.sz

	def place_building_on_grid(self, building, grid_pt):
		map_pt = self.grid_coords_to_map_coords(grid_pt) + self.tile_sz * 0.5
		self.place_building(building, map_pt)

	def place_building(self, building, pt):
		if pt not in self:
			raise TileMapException("Buildings must be placed in bounds")
		# TODO: Compute building overlaps here
		#if self.get_building_at_position(x, y) is not None:
		#    raise TileMapException("There is already a building at that position")
		self.building_registry[building.building_id] = {
			'building' : building,
			'position' : pt,
			}

	def place_unit_on_grid(self, building, grid_pt):
		map_pt = self.grid_coords_to_map_coords(grid_pt) + self.tile_sz * 0.5
		self.place_unit(building, map_pt)

	def place_unit(self, unit, pt):
		if pt not in self:
			raise TileMapException("Units must be placed in bounds")
		self.unit_registry[unit.unit_id] = {
			'unit'     : unit,
			'position' : pt,
			}
		unit.set_tile_map(self)

	def get_units(self):
		return [ v['unit'] for v in self.unit_registry.values() ]

	def get_buildings(self):
		return [ v['building'] for v in self.building_registry.values() ]

	def move_unit(self, unit, v):
		"""
		Move the unit's position by a direction vector

		args:
		v (Vector): the vector by which to move the unit's position
		"""
		# TODO: add error checks
		new_position = self.get_unit_position(unit) + v
		new_terrain = self.get_terrain(new_position)
		if (new_terrain.is_water != unit.moves_on_water):
				return #returns without error so the unit just stops
		# TODO: Should we clamp this position in bounds or error if it goes out?
		# This will be handled by the interface.  Shouldn't be possible to order it out of bounds.
		if new_position not in self:
			raise TileMapException("Unit may not move out of bounds")
		self.set_unit_position(unit, new_position)

	def get_unit_position(self, unit):
		if unit.unit_id not in self.unit_registry:
			raise TileMapException("That unit has not been added to the tile map: {}".format(unit))
		return self.unit_registry[unit.unit_id]['position']

	def set_unit_position(self, unit, pt):
		if unit.unit_id not in self.unit_registry:
			raise TileMapException("That unit has not been added to the tile map: {}".format(unit))
		self.unit_registry[unit.unit_id]['position'] = pt

	def get_unit_at_position(self, pt):
		for unit in self.get_units():
			if (unit.pt - pt).M < min(self.tile_sz.w, self.tile_sz.h) / 2:
				return unit
		return None

	def select_unit(self, unit):
		self.selected_unit = unit

	def clear_unit_selection(self):
		self.selected_unit = None

	def get_tile(self, pt):
		if pt not in self:
			raise TileMapException("out of bounds: ".format(pt))
		return self.tile_grid.get_tile(self.map_coords_to_grid_coords(pt))

	def get_unit_at_position(self, pt):
		for unit in self.get_units():
			if (unit.pt - pt).M < min(self.tile_sz.w, self.tile_sz.h) / 2:
				return unit

	def select_unit(self, unit):
		self.selected_unit = unit

	def clear_unit_selection(self):
		self.selected_unit = None

	def get_tile_under_unit(self, unit):
		if unit.unit_id not in self.unit_registry:
			raise TileMapException("That unit has not been added to the tile map: {}".format(unit))
		return self.get_tile(self.get_unit_position(unit))

	def get_building_position(self, building):
		if building.building_id not in self.building_registry:
			raise TileMapException("That building has not been added to the tile map: {}".format(building))
		return self.building_registry[building.building_id]['position']

	def get_building_at_position(self, pt):
		# TODO: this should actually check to see if the point is within the buildings bounds when buildings are given a boundary
		for building in self.get_buildings():
			if (self.building_registry[building.building_id]['position'] - pt).M < min(self.tile_sz.w, self.tile_sz.h) / 2:
				return building

	def get_tile(self, pt):
		if pt not in self:
			raise TileMapException("out of bounds: ".format(pt))
		return self.tile_grid.get_tile(self.map_coords_to_grid_coords(pt))

	def get_terrain(self, pt):
		tile = self.get_tile(pt)
		return tile.terrain

	def map_coords_to_grid_coords(self, pt):
		"""
		Converts a point on the map to a point on the grid
		"""
		return Point(int(pt.x / self.tile_sz.w), int(pt.y / self.tile_sz.h))

	def grid_coords_to_map_coords(self, pt):
		return pt * self.tile_sz

	def __contains__(self, pt):
		return pt in self.bounds_rect
