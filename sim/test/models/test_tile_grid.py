import unittest
from sim.models.tile_grid import TileGrid, TileGridException
from sim.models.tile import Tile

class TileGridModelTest(unittest.TestCase):

	def test_initialization_creates_a_grid_of_tiles(self):
		grid = TileGrid(10, 15)
		for (x, y) in [ (x, y) for x in range(10) for y in range(15) ]:
			self.assertIsInstance(grid.tile_array[x, y], Tile)

	def test_initialization_dies_if_w_or_h_is_not_greater_than_0(self):
		with self.assertRaises(TileGridException) as error_context:
			TileGrid(0, 10)
		self.assertEqual(
			error_context.exception.message,
			"Tile grid must have a positive width and height",
			)

		with self.assertRaises(TileGridException) as error_context:
			TileGrid(10, 0)
		self.assertEqual(
			error_context.exception.message,
			"Tile grid must have a positive width and height",
			)

	def test_in_bounds_returns_true_if_the_requested_coordinates_are_within_the_grid(self):
		grid = TileGrid(10, 15)

		self.assertTrue(grid.in_bounds(5, 5))
		self.assertFalse(grid.in_bounds(-1,  5))
		self.assertFalse(grid.in_bounds( 5, -1))
		self.assertFalse(grid.in_bounds(10,  5))
		self.assertFalse(grid.in_bounds( 5, 15))

	def test_get_tile_raises_an_exception_if_the_requested_coordinates_are_out_of_bounds(self):
		grid = TileGrid(10, 15)

		with self.assertRaises(TileGridException) as error_context:
			grid.get_tile(-1, 5)
		self.assertIn("out of bounds", error_context.exception.message)

	def test_get_tiles_in_rect_returns_all_tiles_within_a_bounding_rectangle(self):
		grid = TileGrid(10, 15)
		tiles_in_rect = grid.get_tiles_in_rect(3, 4, 2, 3)
		self.assertEqual(6, len(tiles_in_rect))
		self.assertIn("(3,4)", [ t.tile_id for t in tiles_in_rect ])
		self.assertIn("(3,6)", [ t.tile_id for t in tiles_in_rect ])
		self.assertIn("(4,4)", [ t.tile_id for t in tiles_in_rect ])
		self.assertIn("(4,6)", [ t.tile_id for t in tiles_in_rect ])

		self.assertNotIn("(3,3)", [ t.tile_id for t in tiles_in_rect ])
		self.assertNotIn("(4,7)", [ t.tile_id for t in tiles_in_rect ])

