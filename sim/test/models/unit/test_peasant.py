import unittest
from sim.models.tile_grid import TileGrid
from sim.models.tile_map import TileMap
from sim.models.unit.peasant import Peasant
from sim.models.terrain import Forest, Plains
from sim.models.resource import Wood
from sim.models.building.cabbage_farm import CabbageFarm

class PeasantModelTest(unittest.TestCase):

	def test_chop_wood_adds_wood_to_the_peasants_cargo_and_adds_addional_chop_wood_action_to_its_action_queue_if_the_quantity_was_greater_than_1(self):
		grid = TileGrid(10, 10)
		tmap = TileMap(grid, 20)
		grid.get_tile(5, 5).set_terrain(Forest)
		serf = Peasant()
		tmap.place_unit(serf, 110, 110)
		self.assertTrue(serf.can_chop_wood())
		serf.chop_wood(1.0, quantity=2)
		self.assertEqual(serf.deliver_cargo(Wood, 5), 1)
		self.assertEqual(len(serf.action_queue), 1)
		serf.act(1.0)
		self.assertEqual(serf.deliver_cargo(Wood, 5), 1)
		self.assertEqual(len(serf.action_queue), 0)

	def test_chop_wood_does_nothing_if_the_current_terrain_is_not_forest(self):
		grid = TileGrid(10, 10)
		tmap = TileMap(grid, 20)
		grid.get_tile(5, 5).set_terrain(Forest)
		serf = Peasant()
		tmap.place_unit(serf, 0, 0)
		serf.chop_wood(1.0)
		self.assertEqual(serf.deliver_cargo(Wood, 5), 0)
		self.assertEqual(len(serf.action_queue), 0)

	def test_chop_wood_does_nothing_if_the_peasant_has_no_more_capacity_to_carry_wood(self):
		grid = TileGrid(10, 10)
		tmap = TileMap(grid, 20)
		grid.get_tile(5, 5).set_terrain(Plains)
		serf = Peasant()
		serf.container.weight_capacity = Wood.weight - 1
		tmap.place_unit(serf, 110, 110)
		serf.chop_wood(1.0)
		self.assertEqual(serf.deliver_cargo(Wood, 5), 0)
		self.assertEqual(len(serf.action_queue), 0)

	def test_check_for_wood_to_chop_adds_a_chop_wood_action_to_the_action_queue_if_the_unit_can_currently_chop_wood(self):
		grid = TileGrid(10, 10)
		tmap = TileMap(grid, 20)
		grid.get_tile(5, 5).set_terrain(Forest)
		serf = Peasant()
		tmap.place_unit(serf, 110, 110)
		serf.check_for_wood_to_chop(1.0)
		self.assertEqual(len(serf.action_queue), 1)
		serf.act(1.0)
		self.assertEqual(serf.deliver_cargo(Wood, 5), 1)
		self.assertEqual(len(serf.action_queue), 0)

	# TODO:test cabbage_farm_creation

