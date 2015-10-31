from sim.models import terrain

class TerrainMap:

	def __init__(self, x_min, y_min, x_max, y_max):
		assert x_max > x_min
		(self.x_min, self.x_max) = (x_min, x_max)
		
		assert y_max > y_min
		(self.y_min, self.y_max) = (y_min, y_max)
		
		self.tile_array = {}
		for x in range(x_min, x_max):
			for y in range(y_min, y_max):
				self.tile_array[x, y] = terrain.Terrain

	def set_terrain(self, terrain, x, y):
		assert x >= self.x_min and x < self.x_max
		assert y >= self.y_min and y < self.y_max
		self.tile_array[x, y] = terrain

	def get_terrain(self, x, y):
		assert x >= self.x_min and x < self.x_max
		assert y >= self.y_min and y < self.y_max
		return self.tile_array[x, y]

	def in_bounds(self, new_x, new_y):
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
