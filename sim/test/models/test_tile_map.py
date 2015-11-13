import unittest
from sim.geometry import Point, Size, Vector, Rectangle
from sim.models.unit.peasant import Peasant
from sim.models.tile_grid import TileGrid
from sim.models.tile_map import TileMap, TileMapException
from sim.models.terrain import Terrain, Forest
from sim.models.building.cabbage_farm import CabbageFarm
from sim.models.terrain_improvement import TerrainImprovement

class TileMapModelTest(unittest.TestCase):

	def test_initialization_raises_an_exception_if_the_tile_width_is_not_positive(self):
		with self.assertRaises(TileMapException) as error_context:
			TileMap(TileGrid(Size(10, 10)), tile_sz=Size(0,0))
		self.assertIn("The tile size must have positive area", error_context.exception.message)

	def test_place_building_puts_a_building_into_the_building_registry_at_the_given_position(self):
		tmap = TileMap(TileGrid(Size(10, 10)))
		farm = CabbageFarm()
		tmap.place_building(farm, Point(50, 50))
		self.assertIn(farm.building_id, tmap.building_registry)
		self.assertEqual(tmap.get_building_position(farm), Point(50, 50))
		#self.assertIs(tmap.get_building_at_position(5, 5), farm)

	def test_place_building_raises_an_exception_when_a_building_is_placed_out_of_bounds(self):
		tmap = TileMap(TileGrid(Size(10, 10)))
		farm = CabbageFarm()
		with self.assertRaises(TileMapException) as error_context:
			tmap.place_building(farm, Point(200, 200))
		self.assertEqual(error_context.exception.message, 'Buildings must be placed in bounds')
		with self.assertRaises(TileMapException) as error_context:
			tmap.place_building(farm, Point(-1, -1))
		with self.assertRaises(TileMapException) as error_context:
			tmap.place_building(farm, Point(-1, 0))
		with self.assertRaises(TileMapException) as error_context:
			tmap.place_building(farm, Point(0, -1))
		with self.assertRaises(TileMapException) as error_context:
			tmap.place_building(farm, Point(1, 200))
		with self.assertRaises(TileMapException) as error_context:
			tmap.place_building(farm, Point(200, 1))

	#def test_place_building_raises_an_exception_when_a_building_is_already_occupying_that_position(self):
	#    tmap = TileMap(0, 0, 10, 10)
	#    tmap.place_building(CabbageFarm(), 5, 5)
	#    with self.assertRaises(TileMapException) as error_context:
	#        tmap.place_building(CabbageFarm(), 5, 5)
	#    self.assertEqual(error_context.exception.message, 'There is already a building at that position')

	def test_place_unit_puts_a_unit_into_the_unit_registry_at_the_given_position(self):
		tmap = TileMap(TileGrid(Size(10, 10)))
		serf = Peasant()
		tmap.place_unit(serf, Point(100, 100))
		self.assertIn(serf.unit_id, tmap.unit_registry)
		self.assertEqual(tmap.get_unit_position(serf), Point(100, 100))

	def test_place_unit_raises_an_exception_when_a_unit_is_placed_out_of_bounds(self):
		tmap = TileMap(TileGrid(Size(10, 10)))
		serf = Peasant()
		with self.assertRaises(TileMapException) as error_context:
			tmap.place_unit(serf, Point(200, 200))
		self.assertEqual(error_context.exception.message, 'Units must be placed in bounds')

	def test_get_units_returns_all_units_on_the_map(self):
		tmap = TileMap(TileGrid(Size(10, 10)))
		serf1 = Peasant()
		serf2 = Peasant()
		serf3 = Peasant()
		tmap.place_unit(serf1, Point(0, 0))
		tmap.place_unit(serf2, Point(100, 100))
		tmap.place_unit(serf3, Point(180, 180))
		units = tmap.get_units()
		self.assertEqual(3, len(units))
		self.assertIn(serf1, units)
		self.assertIn(serf2, units)
		self.assertIn(serf3, units)

	def test_get_unit_position_returns_the_location_of_a_unit(self):
		tmap = TileMap(TileGrid(Size(10, 10)))
		serf = Peasant()
		tmap.place_unit(serf, Point(100, 100))
		self.assertEqual(tmap.get_unit_position(serf), Point(100, 100))

	def test_get_unit_position_raises_an_exception_if_the_unit_has_not_been_added_to_the_map(self):
		tmap = TileMap(TileGrid(Size(10, 10)))
		serf = Peasant()
		with self.assertRaises(TileMapException) as error_context:
			tmap.get_unit_position(serf)
		self.assertIn('That unit has not been added to the tile map', error_context.exception.message)

	def test_set_unit_position_sets_the_location_of_a_unit(self):
		tmap = TileMap(TileGrid(Size(10, 10)))
		serf = Peasant()
		tmap.place_unit(serf, Point(100, 100))
		tmap.set_unit_position(serf, Point(20, 20))
		self.assertEqual(tmap.get_unit_position(serf), Point(20, 20))

	def test_set_unit_position_raises_an_exception_if_the_unit_has_not_been_added_to_the_map(self):
		tmap = TileMap(TileGrid(Size(10, 10)))
		serf = Peasant()
		with self.assertRaises(TileMapException) as error_context:
			tmap.set_unit_position(serf, Point(100, 100))
		self.assertIn('That unit has not been added to the tile map', error_context.exception.message)

	def test_get_building_position_returns_the_location_of_a_building(self):
		tmap = TileMap(TileGrid(Size(10, 10)))
		farm = CabbageFarm()
		tmap.place_building(farm, Point(100, 100))
		self.assertEqual(tmap.get_building_position(farm), Point(100, 100))

	def test_get_building_position_raises_an_exception_if_the_unit_has_not_been_added_to_the_map(self):
		tmap = TileMap(TileGrid(Size(10, 10)))
		farm = CabbageFarm()
		with self.assertRaises(TileMapException) as error_context:
			tmap.get_building_position(farm)
		self.assertIn('That building has not been added to the tile map', error_context.exception.message)

	#def test_get_building_at_position_returns_a_building_at_a_specific_location(self):
	#    tmap = TileMap(TileGrid(10, 10), 20)
	#    farm = CabbageFarm()
	#    tmap.place_building(farm, 100, 100)
	#    self.assertIs(tmap.get_building_at_position(100, 100), farm)

	#def test_get_building_at_position_returns_None_if_there_is_no_building_at_that_location(self):
	#    tmap = TileMap(0, 0, 10, 10)
	#    self.assertIs(tmap.get_building_at_position(5, 5), None)

	def test_get_tile_under_unit_returns_the_tile_at_the_units_position(self):
		tmap = TileMap(TileGrid(Size(10, 10)))
		serf = Peasant()
		tmap.place_unit(serf, Point(110, 110))
		tile = tmap.tile_grid.get_tile(Point(5, 5))
		tile.tile_id = "target tile"
		self.assertEqual(tmap.get_tile_under_unit(serf).tile_id, "target tile")

	def test_map_coords_to_grid_coords_converts_tile_map_coordinates_to_tile_grid_coordinates(self):
		tmap = TileMap(TileGrid(Size(10, 10)))
		self.assertEqual(Point(10, 15), tmap.map_coords_to_grid_coords(Point(200, 300)))
		self.assertEqual(Point(10, 15), tmap.map_coords_to_grid_coords(Point(219, 319)))
		self.assertEqual(Point(11, 16), tmap.map_coords_to_grid_coords(Point(220, 320)))

	def test_grid_coords_to_map_coords_converts_tile_grid_coordinates_to_tile_map_coordinates(self):
		tmap = TileMap(TileGrid(Size(10, 10)))
		self.assertEqual(Point(200, 300), tmap.grid_coords_to_map_coords(Point(10, 15)))
		self.assertEqual(Point(220, 320), tmap.grid_coords_to_map_coords(Point(11, 16)))

	def test_in_bounds_tests_if_coordinates_are_within_the_tile_map(self):
		tmap = TileMap(TileGrid(Size(10, 10)))
		self.assertTrue(Point(100, 100) in tmap)
		self.assertFalse(Point(200, 100) in tmap)
		self.assertFalse(Point(100, 200) in tmap)
		self.assertFalse(Point( -1, 100) in tmap)
		self.assertFalse(Point(100,  -1) in tmap)

	def test_move_unit_moves_a_unit_on_the_map(self):
		tmap = TileMap(TileGrid(Size(10, 10)))
		serf = Peasant()
		tmap.place_unit(serf, Point(55, 75))
		tmap.move_unit(serf, Vector(-5, 10))
		self.assertEqual(tmap.get_unit_position(serf), Point(50, 85))

