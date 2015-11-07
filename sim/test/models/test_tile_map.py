import unittest
from sim.models.unit.peasant import Peasant
from sim.models.tile_map import TileMap, TileMapException
from sim.models.terrain import Terrain, Forest
from sim.models.building.cabbage_farm import CabbageFarm
from sim.models.terrain_improvement import TerrainImprovement

class TileMapModelTest(unittest.TestCase):

    def test_initialization_populates_a_map_of_generic_terrain(self):
        tmap = TileMap(0, 0, 10, 10)
        for (x, y) in [ (x, y) for x in range(10) for y in range(10) ]:
            self.assertIs(tmap.tile_array[x, y].terrain_type, Terrain)

    def test_place_building_puts_a_building_into_the_building_registry_at_the_given_position(self):
        tmap = TileMap(0, 0, 10, 10)
        farm = CabbageFarm()
        tmap.place_building(farm, 5, 5)
        self.assertIn(farm.building_id, tmap.building_registry)
        self.assertEqual(tmap.get_building_position(farm), (5, 5))
        self.assertIs(tmap.get_building_at_position(5, 5), farm)

    def test_place_building_raises_an_exception_when_a_building_is_placed_out_of_bounds(self):
        tmap = TileMap(0, 0, 10, 10)
        farm = CabbageFarm()
        with self.assertRaises(TileMapException) as error_context:
            tmap.place_building(farm, 10, 10)
        self.assertEqual(error_context.exception.message, 'Buildings must be placed in bounds')
        with self.assertRaises(TileMapException) as error_context:
            tmap.place_building(farm, -1, -1)
        with self.assertRaises(TileMapException) as error_context:
            tmap.place_building(farm, -1, 0)
        with self.assertRaises(TileMapException) as error_context:
            tmap.place_building(farm, 0, -1)
        with self.assertRaises(TileMapException) as error_context:
            tmap.place_building(farm, 9, 10)
        with self.assertRaises(TileMapException) as error_context:
            tmap.place_building(farm, 10, 9)

    def test_place_building_raises_an_exception_when_a_building_is_already_occupying_that_position(self):
        tmap = TileMap(0, 0, 10, 10)
        tmap.place_building(CabbageFarm(), 5, 5)
        with self.assertRaises(TileMapException) as error_context:
            tmap.place_building(CabbageFarm(), 5, 5)
        self.assertEqual(error_context.exception.message, 'There is already a building at that position')

    def test_place_unit_puts_a_unit_into_the_unit_registry_at_the_given_position(self):
        tmap = TileMap(0, 0, 10, 10)
        serf = Peasant()
        tmap.place_unit(serf, 5, 5)
        self.assertIn(serf.unit_id, tmap.unit_registry)
        self.assertEqual(tmap.get_unit_position(serf), (5, 5))

    def test_place_unit_raises_an_exception_when_a_unit_is_placed_out_of_bounds(self):
        tmap = TileMap(0, 0, 10, 10)
        serf = Peasant()
        with self.assertRaises(TileMapException) as error_context:
            tmap.place_unit(serf, 10, 10)
        self.assertEqual(error_context.exception.message, 'Units must be placed in bounds')

    def test_get_units_returns_all_units_on_the_map(self):
        tmap = TileMap(0, 0, 10, 10)
        serf1 = Peasant()
        serf2 = Peasant()
        serf3 = Peasant()
        tmap.place_unit(serf1, 0, 0)
        tmap.place_unit(serf2, 5, 5)
        tmap.place_unit(serf3, 9, 9)
        units = tmap.get_units()
        self.assertEqual(3, len(units))
        self.assertIn(serf1, units)
        self.assertIn(serf2, units)
        self.assertIn(serf3, units)

    def test_get_unit_position_returns_the_location_of_a_unit(self):
        tmap = TileMap(0, 0, 10, 10)
        serf = Peasant()
        tmap.place_unit(serf, 5, 5)
        self.assertEqual(tmap.get_unit_position(serf), (5, 5))

    def test_get_unit_position_raises_an_exception_if_the_unit_has_not_been_added_to_the_map(self):
        tmap = TileMap(0, 0, 10, 10)
        serf = Peasant()
        with self.assertRaises(TileMapException) as error_context:
            tmap.get_unit_position(serf)
        self.assertIn('That unit has not been added to the tile map', error_context.exception.message)

    def test_set_unit_position_sets_the_location_of_a_unit(self):
        tmap = TileMap(0, 0, 10, 10)
        serf = Peasant()
        tmap.place_unit(serf, 5, 5)
        tmap.set_unit_position(serf, 1, 1)
        self.assertEqual(tmap.get_unit_position(serf), (1, 1))

    def test_set_unit_position_raises_an_exception_if_the_unit_has_not_been_added_to_the_map(self):
        tmap = TileMap(0, 0, 10, 10)
        serf = Peasant()
        with self.assertRaises(TileMapException) as error_context:
            tmap.set_unit_position(serf, 5, 5)
        self.assertIn('That unit has not been added to the tile map', error_context.exception.message)

    def test_get_building_position_returns_the_location_of_a_building(self):
        tmap = TileMap(0, 0, 10, 10)
        farm = CabbageFarm()
        tmap.place_building(farm, 5, 5)
        self.assertEqual(tmap.get_building_position(farm), (5, 5))

    def test_get_building_position_raises_an_exception_if_the_unit_has_not_been_added_to_the_map(self):
        tmap = TileMap(0, 0, 10, 10)
        farm = CabbageFarm()
        with self.assertRaises(TileMapException) as error_context:
            tmap.get_building_position(farm)
        self.assertIn('That building has not been added to the tile map', error_context.exception.message)

    def test_get_building_at_position_returns_a_building_at_a_specific_location(self):
        tmap = TileMap(0, 0, 10, 10)
        farm = CabbageFarm()
        tmap.place_building(farm, 5, 5)
        self.assertIs(tmap.get_building_at_position(5, 5), farm)

    def test_get_building_at_position_returns_None_if_there_is_no_building_at_that_location(self):
        tmap = TileMap(0, 0, 10, 10)
        self.assertIs(tmap.get_building_at_position(5, 5), None)

    def test_get_terrain_under_unit_returns_the_terrain_at_the_units_position(self):
        tmap = TileMap(0, 0, 10, 10)
        serf = Peasant()
        tmap.place_unit(serf, 5, 5)
        tmap.set_terrain(Forest, 5, 5)
        self.assertIs(tmap.get_terrain_under_unit(serf), Forest)

