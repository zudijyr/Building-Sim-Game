import unittest
from sim.models.tile_grid import TileGrid, TileGridException
from sim.models.tile import Tile
from sim.geometry import Size, Point, Rectangle

class TileGridModelTest(unittest.TestCase):

	def test_initialization_creates_a_grid_of_tiles(self):
		grid = TileGrid(Size(10, 15))
		for pt in [ Point(x, y) for x in range(10) for y in range(15) ]:
			self.assertIsInstance(grid.tile_array[pt], Tile)

	def test_initialization_dies_area_of_tile_grid_is_zero(self):
		with self.assertRaises(TileGridException) as error_context:
			TileGrid(Size(0, 10))
		self.assertEqual(error_context.exception.message, "The grid must have positive area")

		with self.assertRaises(TileGridException) as error_context:
			TileGrid(Size(10, 0))
		self.assertEqual(error_context.exception.message, "The grid must have positive area")

	def test___contains___returns_true_if_the_requested_point_is_within_the_grid(self):
		grid = TileGrid(Size(10, 15))

		self.assertTrue(Point(5, 5) in grid)
		self.assertFalse(Point(-1,  5) in grid)
		self.assertFalse(Point( 5, -1) in grid)
		self.assertFalse(Point(10,  5) in grid)
		self.assertFalse(Point( 5, 15) in grid)

	def test_get_tile_raises_an_exception_if_the_requested_point_is_out_of_bounds(self):
		grid = TileGrid(Size(10, 15))

		with self.assertRaises(TileGridException) as error_context:
			grid.get_tile(Point(-1, 5))
		self.assertIn("out of bounds", error_context.exception.message)

	def test_get_tiles_in_rect_returns_all_tiles_within_a_bounding_rectangle(self):
		grid = TileGrid(Size(10, 15))
		tiles_in_rect = grid.get_tiles_in_rect(Rectangle(Point(3, 4), Size(2, 3)))
		self.assertEqual(6, len(tiles_in_rect))
		self.assertIn("(3,4)", [ t.tile_id for t in tiles_in_rect ])
		self.assertIn("(3,6)", [ t.tile_id for t in tiles_in_rect ])
		self.assertIn("(4,4)", [ t.tile_id for t in tiles_in_rect ])
		self.assertIn("(4,6)", [ t.tile_id for t in tiles_in_rect ])

		self.assertNotIn("(3.0,3.0)", [ t.tile_id for t in tiles_in_rect ])
		self.assertNotIn("(4.0,7.0)", [ t.tile_id for t in tiles_in_rect ])

