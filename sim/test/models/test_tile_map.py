import unittest
from sim.geometry import Point, Size, Vector, Rectangle
from sim.models.unit.peasant import Peasant
from sim.models.unit.ship import Ship
from sim.models.tile_grid import TileGrid
from sim.models.tile_map import TileMap, TileMapException
from sim.models.terrain import Terrain, Forest, Water, Grass
from sim.models.building.cabbage_farm import CabbageFarm
from sim.models.terrain_improvement import TerrainImprovement

class TileMapModelTest(unittest.TestCase):

	def test_initialization_raises_an_exception_if_the_tile_size_has_an_area_of_zero(self):
		with self.assertRaises(TileMapException) as error_context:
			TileMap(TileGrid(Size(10, 10)), tile_sz=Size(0,0))
		self.assertIn("The tile size must have positive area", error_context.exception.message)

	def test_place_building_on_grid_puts_a_building_onto_the_map_in_the_specified_grid_cell(self):
		tmap = TileMap(TileGrid(Size(10, 10)), tile_sz=Size(20, 20))
		farm = CabbageFarm()
		tmap.place_building_on_grid(farm, Point(5, 5))
		self.assertIn(farm.building_id, tmap.building_registry)
		self.assertEqual(tmap.get_building_position(farm), Point(5*20+0.5*20, 5*20+0.5*20))

	def test_place_building_puts_a_building_into_the_building_registry_at_the_given_position(self):
		tmap = TileMap(TileGrid(Size(10, 10)))
		farm = CabbageFarm()
		tmap.place_building(farm, Point(50, 50))
		self.assertIn(farm.building_id, tmap.building_registry)
		self.assertEqual(tmap.get_building_position(farm), Point(50, 50))

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

	def test_place_unit_on_grid_puts_a_unit_onto_the_map_in_the_specified_grid_cell(self):
		tmap = TileMap(TileGrid(Size(10, 10)), tile_sz=Size(20, 20))
		serf = Peasant()
		tmap.place_unit_on_grid(serf, Point(5, 5))
		self.assertIn(serf.unit_id, tmap.unit_registry)
		self.assertEqual(tmap.get_unit_position(serf), Point(5*20+0.5*20, 5*20+0.5*20))

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

	def test_get_buildings_returns_all_buildings_on_the_map(self):
		tmap = TileMap(TileGrid(Size(10, 10)))
		building1 = CabbageFarm()
		building2 = CabbageFarm()
		building3 = CabbageFarm()
		tmap.place_building(building1, Point(0, 0))
		tmap.place_building(building2, Point(100, 100))
		tmap.place_building(building3, Point(180, 180))
		buildings = tmap.get_buildings()
		self.assertEqual(3, len(buildings))
		self.assertIn(building1, buildings)
		self.assertIn(building2, buildings)
		self.assertIn(building3, buildings)

	def test_move_unit_moves_a_unit_on_the_map(self):
		tmap = TileMap(TileGrid(Size(10, 10)))
		serf = Peasant()
		tmap.place_unit(serf, Point(55, 75))
		tmap.move_unit(serf, Vector(-5, 10))
		self.assertEqual(tmap.get_unit_position(serf), Point(50, 85))

	def test_move_unit_raises_an_exception_if_the_move_would_take_the_unit_out_of_bounds(self):
		tmap = TileMap(TileGrid(Size(10, 10)))
		serf = Peasant()
		tmap.place_unit(serf, Point(5, 5))
		with self.assertRaises(TileMapException) as error_context:
			tmap.move_unit(serf, Vector(-5, -10))
		self.assertIn("out of bounds", error_context.exception.message)

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

	def test_get_unit_at_position_finds_a_unit_near_to_the_given_point(self):
		tmap = TileMap(TileGrid(Size(10, 10)))
		serf = Peasant()
		tmap.place_unit(serf, Point(100, 100))
		self.assertIs(serf, tmap.get_unit_at_position(Point(95, 95)))

	def test_get_unit_at_position_returns_None_if_there_is_no_unit_near_the_given_point(self):
		tmap = TileMap(TileGrid(Size(10, 10)))
		serf = Peasant()
		tmap.place_unit(serf, Point(100, 100))
		self.assertIsNone(tmap.get_unit_at_position(Point(50, 50)))

	def test_get_tile_returns_a_tile_at_a_given_position(self):
		grid = TileGrid(Size(2, 2))
		grid.get_tile(Point(1, 1)).tile_id = 'target'
		tmap = TileMap(grid, tile_sz=Size(10, 10))
		tile = tmap.get_tile(Point(15, 15))
		self.assertEqual(tile.tile_id, 'target')

	def test_get_tile_raises_an_exception_when_the_requested_position_is_out_of_bounds(self):
		tmap = TileMap(TileGrid(Size(2, 2)))
		with self.assertRaises(TileMapException) as error_context:
			tmap.get_tile(Point(-1, 0))
		self.assertIn("out of bounds", error_context.exception.message)

	def test_get_tile_under_unit_returns_the_tile_at_the_units_position(self):
		tmap = TileMap(TileGrid(Size(10, 10)))
		serf = Peasant()
		tmap.place_unit(serf, Point(110, 110))
		tile = tmap.tile_grid.get_tile(Point(5, 5))
		tile.tile_id = "target tile"
		self.assertEqual(tmap.get_tile_under_unit(serf).tile_id, "target tile")

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

	def test_get_building_at_position_finds_a_building_near_to_the_given_point(self):
		tmap = TileMap(TileGrid(Size(10, 10)))
		farm = CabbageFarm()
		tmap.place_building(farm, Point(100, 100))
		self.assertIs(farm, tmap.get_building_at_position(Point(95, 95)))

	def test_get_building_at_position_returns_None_if_there_is_no_building_near_the_given_point(self):
		tmap = TileMap(TileGrid(Size(10, 10)))
		farm = CabbageFarm()
		tmap.place_building(farm, Point(100, 100))
		self.assertIsNone(tmap.get_building_at_position(Point(50, 50)))

	def test_map_coords_to_grid_coords_converts_tile_map_coordinates_to_tile_grid_coordinates(self):
		tmap = TileMap(TileGrid(Size(10, 10)))
		self.assertEqual(Point(10, 15), tmap.map_coords_to_grid_coords(Point(200, 300)))
		self.assertEqual(Point(10, 15), tmap.map_coords_to_grid_coords(Point(219, 319)))
		self.assertEqual(Point(11, 16), tmap.map_coords_to_grid_coords(Point(220, 320)))

	def test_grid_coords_to_map_coords_converts_tile_grid_coordinates_to_tile_map_coordinates(self):
		tmap = TileMap(TileGrid(Size(10, 10)))
		self.assertEqual(Point(200, 300), tmap.grid_coords_to_map_coords(Point(10, 15)))
		self.assertEqual(Point(220, 320), tmap.grid_coords_to_map_coords(Point(11, 16)))

	def test___contains___tests_if_coordinates_are_within_the_tile_map(self):
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

