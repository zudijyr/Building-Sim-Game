from sim import SimException
from sim.models.tile import Tile
from sim.geometry import *

class TileGridException(SimException): pass

class TileGrid:
	"""
	NOTE: x, y coordinates within the context of this TileGrid object refer
		  to the placement within the grid not on the map in general

		  It would probably be good to do the tile coordinates in terms of
		  (i, j) (row, column) instead of x, y to emphasize the difference
	"""

	def __init__(self, sz):
		if sz.w <= 0 or sz.h <= 0:
			raise TileGridException("The grid must have positive area")
		self.bounds_rect = Rectangle(Point(0, 0), Size(int(sz.w), int(sz.h)))

		self.tile_array = {}
		for x in range(self.w):
			for y in range(self.h):
				pt = Point(x,y)
				self.tile_array[pt] = Tile(tile_id="{}".format(pt))
	@property
	def sz(self):
		return self.bounds_rect.sz

	@property
	def w(self):
		return self.bounds_rect.w

	@property
	def h(self):
		return self.bounds_rect.h

	def get_tile(self, pt):
		if pt not in self:
			raise TileGridException("out of bounds: {}".format(pt))
		return self.tile_array[pt]

	def __contains__(self, pt):
		return pt in self.bounds_rect

	def get_grid_points_in_rect(self, r=None):
		if r is None:
			r = self.bounds_rect
		if r.p not in self or r.p + r.sz + Vector(-1, -1) not in self:
			raise TileGridException("invalid rectangle: ".format(r))
		for rx in range(r.p.x, r.p.x + r.w):
			for ry in range(r.p.y, r.p.y + r.h):
				yield Point(rx, ry)

	def get_tiles_in_rect(self, r):
		if r.p not in self or r.p + r.sz + Vector(-1, -1) not in self:
			raise TileGridException("invalid rectangle: ".format(r))
		return [ self.get_tile(pt) for pt in self.get_grid_points_in_rect(r) ]

