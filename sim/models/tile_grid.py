from sim import SimException
from sim.models.tile import Tile

class TileGridException(SimException): pass

class TileGrid:
	"""
	NOTE: x, y coordinates within the context of this TileGrid object refer
		  to the placement within the grid not on the map in general

		  It would probably be good to do the tile coordinates in terms of
		  (i, j) (row, column) instead of x, y to emphasize the difference
	"""

	def __init__(self, w, h):
		if w <= 0 or h <= 0:
			raise TileGridException("Tile grid must have a positive width and height")
		(self.w, self.h) = (w, h)

		self.tile_array = {}
		for x in range(w):
			for y in range(h):
				self.tile_array[x, y] = Tile(tile_id="({},{})".format(x, y))

	def get_tile(self, x, y):
		if not self.in_bounds(x, y):
			raise TileGridException("out of bounds: ({}, {})".format(x, y))
		return self.tile_array[x, y]

	def in_bounds(self, x, y):
		if x >= 0 and x < self.w and y >= 0 and y < self.h:
			return True
		else:
			return False

	def get_tiles_in_rect(self, x, y, w, h):
		if not self.in_bounds(x, y) and self.in_bounds(x + w - 1, y + h - 1):
			raise TileGridException("invalid rectangle: ({}, {}, {}, {})".format(x, y, w, h))
		return [ self.get_tile(rx, ry) for rx in range(x, x + w) for ry in range(y, y + h) ]
