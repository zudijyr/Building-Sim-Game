import unittest
from sim.models.tile_grid import TileGrid, TileGridException
from sim.models.tile import Tile
from sim.geometry import Size, Point, Rectangle


class TileGridModelTest(unittest.TestCase):

	def test_initialization_creates_a_grid_of_tiles(self):
		grid = TileGrid(Size(10, 15))
		for pt in [Point(x, y) for x in range(10) for y in range(15)]:
			self.assertIsInstance(grid.tile_array[pt], Tile)

	def test_initialization_dies_if_the_area_of_tile_grid_is_zero(self):
		with self.assertRaises(TileGridException) as error_context:
			TileGrid(Size(0, 10))
		self.assertEqual(
			error_context.exception.message,
			"The grid must have positive area",
			)

		with self.assertRaises(TileGridException) as error_context:
			TileGrid(Size(10, 0))
		self.assertEqual(
			error_context.exception.message,
			"The grid must have positive area",
			)

	def test___contains___returns_true_if_the_requested_point_is_within_the_grid(self):  # noqa
		grid = TileGrid(Size(10, 15))

		self.assertTrue(Point(5, 5) in grid)
		self.assertFalse(Point(-1, 5) in grid)
		self.assertFalse(Point(5, -1) in grid)
		self.assertFalse(Point(10, 5) in grid)
		self.assertFalse(Point(5, 15) in grid)

	def test_get_tile_raises_an_exception_if_the_requested_point_is_out_of_bounds(self):  # noqa
		grid = TileGrid(Size(10, 15))

		with self.assertRaises(TileGridException) as error_context:
			grid.get_tile(Point(-1, 5))
		self.assertIn("out of bounds", error_context.exception.message)

	def test_get_grid_points_in_rect_finds_all_points_inside_of_a_bounding_rectangle(self):  # noqa
		grid = TileGrid(Size(10, 15))
		rect = Rectangle(Point(4, 5), Size(2, 3))
		expected_points = [
			Point(x, y) for x in range(4, 4+2) for y in range(5, 5+3)
			]
		computed_points = [pt for pt in grid.get_grid_points_in_rect(rect)]
		self.assertEqual(expected_points, computed_points)

	def test_get_grid_points_in_rect_raises_an_error_if_the_bounding_rect_is_out_of_bounds(self):  # noqa
		grid = TileGrid(Size(10, 15))
		rect = Rectangle(Point(8, 13), Size(4, 4))
		with self.assertRaises(TileGridException) as error_context:
			grid.get_grid_points_in_rect(rect)
		self.assertIn("invalid rectangle", error_context.exception.message)

	def test_get_grid_points_in_rect_finds_all_points_inside_of_the_grid_if_a_rectangle_is_not_provided(self):  # noqa
		grid = TileGrid(Size(10, 15))
		expected_points = [Point(x, y) for x in range(10) for y in range(15)]
		computed_points = [pt for pt in grid.get_grid_points_in_rect()]
		self.assertEqual(expected_points, computed_points)

	def test_get_tiles_in_rect_returns_all_tiles_within_a_bounding_rectangle(self):  # noqa
		grid = TileGrid(Size(10, 15))
		tiles_in_rect = grid.get_tiles_in_rect(
			Rectangle(Point(3, 4), Size(2, 3))
			)
		self.assertEqual(6, len(tiles_in_rect))
		self.assertIn("(3.00,4.00)", [t.tile_id for t in tiles_in_rect])
		self.assertIn("(3.00,6.00)", [t.tile_id for t in tiles_in_rect])
		self.assertIn("(4.00,4.00)", [t.tile_id for t in tiles_in_rect])
		self.assertIn("(4.00,6.00)", [t.tile_id for t in tiles_in_rect])

		self.assertNotIn("(3.00,3.00)", [t.tile_id for t in tiles_in_rect])
		self.assertNotIn("(4.00,7.00)", [t.tile_id for t in tiles_in_rect])
