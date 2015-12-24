from sim.geometry import Point, Rectangle


class Camera:

	def __init__(self, tile_map):
		self.tile_map = tile_map
		self.view_rect = Rectangle(Point(0, 0), tile_map.sz)
		self.minimum_tile_line_in_view = 10

	def convert_world_vector_to_view_vector(self, v):
		return (v / self.tile_map.sz) * self.view_rect.sz

	def convert_world_point_to_view_point(self, p):
		return (p / self.tile_map.sz) * self.view_rect.sz + self.view_rect.p

	def pan(self, v):
		scaled_v = self.convert_world_vector_to_view_vector(v)
		center = self.view_rect.clamp_point(self.view_rect.center + scaled_v)
		clamped_v = center - self.view_rect.center
		self.view_rect = Rectangle(
			self.view_rect.p + clamped_v,
			self.view_rect.sz,
			)

	def zoom(self, z):
		min_sz = self.tile_map.tile_sz * self.minimum_tile_line_in_view
		min_z = max(*(min_sz / self.view_rect.sz))
		max_sz = self.tile_map.sz
		max_z = min(*(max_sz / self.view_rect.sz))
		clamped_z = max(min(z, max_z), min_z)
		self.view_rect = self.view_rect * clamped_z

	@property
	def ortho_matrix(self):
		return (
			self.view_rect.left,
			self.view_rect.right,
			self.view_rect.bottom,
			self.view_rect.top,
			)
