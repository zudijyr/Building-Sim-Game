from sim import SimException
from sim.geometry import Point, Size, Rectangle


class TileMapException(SimException):
	pass


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
		# if self.get_building_at_position(x, y) is not None:
		#     message = "There is already a building at that position"
		#     raise TileMapException(message)
		self.building_registry[building.building_id] = {
			'building': building,
			'position': pt,
			}

	def place_unit_on_grid(self, unit, grid_pt):
		map_pt = self.grid_coords_to_map_coords(grid_pt) + self.tile_sz * 0.5
		self.place_unit(unit, map_pt)

	def place_unit(self, unit, pt):
		if pt not in self:
			raise TileMapException("Units must be placed in bounds")
		self.unit_registry[unit.unit_id] = unit
		unit.tile_map = self
		unit.pt = pt

	def get_units(self):
		return self.unit_registry.values()

	def get_buildings(self):
		return [v['building'] for v in self.building_registry.values()]

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

	def get_building_position(self, building):
		if building.building_id not in self.building_registry:
			message = "That building has not been added to the tile map: "
			message += str(building)
			raise TileMapException(message)
		return self.building_registry[building.building_id]['position']

	def get_building_at_position(self, pt):
		# TODO: this should actually check to see if the point is within the
		#       buildings bounds when buildings are given a boundary
		for building in self.get_buildings():
			b_pt = self.building_registry[building.building_id]['position']
			if (b_pt - pt).M < min(self.tile_sz.w, self.tile_sz.h) / 2:
				return building

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
