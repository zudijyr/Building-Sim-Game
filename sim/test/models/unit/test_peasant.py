import unittest
from sim.geometry import *
from sim.models.tile_grid import TileGrid
from sim.models.tile_map import TileMap
from sim.models.unit.peasant import Peasant
from sim.models.terrain import Forest, Plains
from sim.models.terrain_improvement import IronOreDeposit
from sim.models.resource import Wood, Lumber
from sim.models.building.cabbage_farm import CabbageFarm
from sim.models.building.iron_mine import IronMine
from sim.models.action import MoveToward, Harvest, ConstructBuilding

class PeasantModelTest(unittest.TestCase):

	def test_chop_wood_adds_wood_to_the_peasants_cargo_and_adds_addional_chop_wood_action_to_its_action_queue_if_the_quantity_was_greater_than_1(self):
		grid = TileGrid(Size(10, 10))
		tmap = TileMap(grid)
		grid.get_tile(Point(5, 5)).set_terrain(Forest)
		serf = Peasant()
		tmap.place_unit(serf, Point(110, 110))
		self.assertTrue(serf.can_chop_wood())
		serf.chop_wood(1.0, quantity=2)
		self.assertEqual(serf.deliver_cargo(Wood, 5), 1)
		self.assertEqual(len(serf.action_queue), 1)
		serf.act(1.0)
		self.assertEqual(serf.deliver_cargo(Wood, 5), 1)
		self.assertEqual(len(serf.action_queue), 0)

	def test_chop_wood_does_nothing_if_the_current_terrain_is_not_forest(self):
		grid = TileGrid(Size(10, 10))
		tmap = TileMap(grid)
		grid.get_tile(Point(5, 5)).set_terrain(Forest)
		serf = Peasant()
		tmap.place_unit(serf, Point(0, 0))
		serf.chop_wood(1.0)
		self.assertEqual(serf.deliver_cargo(Wood, 5), 0)
		self.assertEqual(len(serf.action_queue), 0)

	def test_chop_wood_does_nothing_if_the_peasant_has_no_more_capacity_to_carry_wood(self):
		grid = TileGrid(Size(10, 10))
		tmap = TileMap(grid)
		grid.get_tile(Point(5, 5)).set_terrain(Plains)
		serf = Peasant()
		serf.container.weight_capacity = Wood.weight - 1
		tmap.place_unit_on_grid(serf, Point(5, 5))
		print(tmap.get_unit_position(serf))
		print(tmap.map_coords_to_grid_coords(tmap.get_unit_position(serf)))
		serf.chop_wood(1.0)
		self.assertEqual(serf.deliver_cargo(Wood, 5), 0)
		self.assertEqual(len(serf.action_queue), 0)

	def test_check_for_wood_to_chop_adds_a_chop_wood_action_to_the_action_queue_if_the_unit_can_currently_chop_wood(self):
		grid = TileGrid(Size(10, 10))
		tmap = TileMap(grid)
		grid.get_tile(Point(5, 5)).set_terrain(Forest)
		serf = Peasant()
		tmap.place_unit(serf, Point(110, 110))
		serf.check_for_wood_to_chop(1.0)
		self.assertEqual(len(serf.action_queue), 1)
		serf.act(1.0)
		self.assertEqual(serf.deliver_cargo(Wood, 5), 1)
		self.assertEqual(len(serf.action_queue), 0)

	def test_peasant_can_build_iron_mine_only_on_iron_ore_deposit(self):
		grid = TileGrid(Size(10, 10))
		tmap = TileMap(grid)
		grid.get_tile(Point(5, 5)).set_terrain_improvement(IronOreDeposit)
		serf1 = Peasant()
		serf1.receive_cargo(Lumber, 10)
		serf2 = Peasant()
		serf2.receive_cargo(Lumber, 10)
		tmap.place_unit(serf1, Point(4, 4))
		tmap.place_unit(serf2, Point(5, 5))
		serf1.set_tile_map(tmap)
		serf2.set_tile_map(tmap)
		serf2.tile.terrain_improvement = IronOreDeposit
		action = ConstructBuilding(IronMine)
		serf1.add_action(ConstructBuilding(IronMine))
		serf2.add_action(ConstructBuilding(IronMine))
		serf1.act(10)
		self.assertEqual(len(tmap.building_registry.values()), 0)
		serf2.act(10)
		self.assertEqual(len(tmap.building_registry.values()), 1) #why does this fail?

	# TODO:test cabbage_farm_creation

