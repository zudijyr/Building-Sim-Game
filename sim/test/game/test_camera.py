import unittest
import numpy
from sim.models.tile_map import TileMap
from sim.models.tile_grid import TileGrid
from sim.geometry import *
from sim.game.camera import Camera

class CameraTest(unittest.TestCase):

	def test_convert_world_vector_to_view_vector_transforms_a_vector_in_world_space_to_a_vector_in_view_space(self):
		tmap = TileMap(TileGrid(Size(12, 16)), tile_sz=Size(10,10))
		cam = Camera(tmap)
		cam.view_rect = Rectangle(Point(2, 3), Size(2, 3))
		self.assertEqual(cam.convert_world_vector_to_view_vector(Vector(3, 4)), Vector(3/120*2, 4/160*3))

	def test_convert_world_point_to_view_point_transforms_a_point_in_world_space_to_a_point_in_view_space(self):
		tmap = TileMap(TileGrid(Size(12, 16)), tile_sz=Size(10,10))
		cam = Camera(tmap)
		cam.view_rect = Rectangle(Point(2, 3), Size(2, 3))
		self.assertEqual(cam.convert_world_point_to_view_point(Point(3, 4)), Point(3/120*2+2, 4/160*3+3))

	def test_pan_moves_the_view_rectangle_by_a_supplied_vector(self):
		tmap = TileMap(TileGrid(Size(12, 16)), tile_sz=Size(10, 10))
		cam = Camera(tmap)
		cam.pan(Vector(3, 4))
		self.assertEqual(cam.view_rect, Rectangle(Point(3, 4), Size(120, 160)))

	def test_pan_clamps_the_center_of_the_camera_within_the_bounds_of_the_map(self):
		tmap = TileMap(TileGrid(Size(12, 16)), tile_sz=Size(10, 10))
		cam = Camera(tmap)
		cam.pan(Vector(-65, 165))
		self.assertEqual(cam.view_rect, Rectangle(Point(-60, 80), Size(120, 160)))

	def test_zoom_scales_the_view_rectangle_by_the_supplied_factor(self):
		tmap = TileMap(TileGrid(Size(12, 16)), tile_sz=Size(10, 10))
		cam = Camera(tmap)
		cam.minimum_tile_line_in_view = 4
		cam.zoom(0.5)
		self.assertEqual(cam.view_rect, Rectangle(Point(30, 40), Size(60, 80)))

	def test_zoom_clamps_the_maximum_zoom_in_to_the_minimum_tile_line_in_view(self):
		tmap = TileMap(TileGrid(Size(12, 16)), tile_sz=Size(10, 10))
		cam = Camera(tmap)
		cam.minimum_tile_line_in_view = 4
		cam.zoom(0.00001)
		expected_r = Rectangle(
			Point(60-4*10/2, 80-4*10*16/12/2),
			Size(    4*10,      4*10*16/12)
			)
		self.assertEqual(cam.view_rect, expected_r)

	def test_zoom_clamps_the_maximum_zoom_out_to_the_size_of_the_map(self):
		tmap = TileMap(TileGrid(Size(12, 16)), tile_sz=Size(10, 10))
		cam = Camera(tmap)
		cam.zoom(1000000)
		self.assertEqual(cam.view_rect, tmap.bounds_rect)

	def test_ortho_matrix_returns_a_cameras_view_rect_as_an_ortho_matrix_friendlly_for_opengl(self):
		""" NOTE: This test is here primarily to satisfy test coverage """
		tmap = TileMap(TileGrid(Size(12, 16)), tile_sz=Size(10,10))
		cam = Camera(tmap)
		self.assertEqual(cam.ortho_matrix, (0, 120, 0, 160))
