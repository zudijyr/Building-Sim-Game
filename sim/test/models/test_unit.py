import unittest
from sim.models.unit import *
from sim.models.terrain_map import TerrainMap
from sim.models.terrain import *
from sim.models.resource import *

class DummyUnit(Unit):
	strength = 10
	movement_speed = 10

class UnitModelTest(unittest.TestCase):

	def test_move_unit_one_moves_the_unit_by_the_specified_change_in_x_and_y(self):
		tmap = TerrainMap(0, 0, 10, 10)
		tmap.set_terrain(Plains, 6,6)
		tmap.set_terrain(Plains, 7,7)
		unit = DummyUnit(5, 5, tmap)
		unit.move_unit_one((1, 1))
		unit.move_unit_one((1, 1))
		self.assertEqual(unit.moves_remaining, 10 - Plains.move_cost * 2)

	def test_move_unit_one_does_not_move_the_unit_if_the_move_would_go_over_the_map_boundary(self):
		tmap = TerrainMap(0, 0, 10, 10)
		unit = DummyUnit(9, 5, tmap)
		unit.move_unit_one((1, 0))
		self.assertEqual(unit.x_position, 9)
		self.assertEqual(unit.y_position, 5)

	def test_move_unit_one_raises_an_exception_if_the_absolute_value_of_the_move_in_x_or_y_is_greater_than_1(self):
		tmap = TerrainMap(0, 0, 10, 10)
		unit = DummyUnit(0, 0, tmap)
		with self.assertRaises(UnitException) as error_context:
			unit.move_unit_one((2, 0))
		self.assertEqual("Must move 1 at a time in x and or y", error_context.exception.message)

	def test_set_path_creates_path_straight_from_initial_to_final_position(self):
		tmap = TerrainMap(0, 0, 10, 10)
		unit = DummyUnit(0, 0, tmap)
		unit.set_path(5,5, tmap)
		self.assertEqual(unit.path, [(1,1),(1,1),(1,1),(1,1),(1,1)] )

	def test_set_path_creates_path_makes_diagonal_moves_first(self):
		tmap = TerrainMap(0, 0, 10, 10)
		unit = DummyUnit(0, 0, tmap)
		unit.set_path(3,5, tmap)
		self.assertEqual(unit.path, [(1,1),(1,1),(1,1),(0,1),(0,1)] )

class PeasantModelTest(unittest.TestCase):

	def test_chop_wood_adds_wood_to_the_peasants_cargo_and_takes_one_move(self):
		tmap = TerrainMap(0, 0, 10, 10)
		tmap.set_terrain(Forest, 5, 5)
		unit = Peasant(5, 5, tmap)
		unit.chop_wood()
		unit.chop_wood()
		self.assertEqual(unit.deliver_cargo(Wood, 5), 2)
		self.assertEqual(unit.moves_remaining, 23)

	def test_chop_wood_does_nothing_if_the_current_terrain_is_not_forest(self):
		tmap = TerrainMap(0, 0, 10, 10)
		tmap.set_terrain(Plains, 5, 5)
		unit = Peasant(5, 5, tmap)
		unit.chop_wood()
		self.assertEqual(unit.deliver_cargo(Wood, 5), 0)
		self.assertEqual(unit.moves_remaining, 25)

	def test_chop_wood_does_nothing_if_the_peasant_has_no_more_capacity_to_carry_wood(self):
		tmap = TerrainMap(0, 0, 10, 10)
		tmap.set_terrain(Forest, 5, 5)
		unit = Peasant(5, 5, tmap)
		unit.container.weight_capacity = Wood.weight - 1
		unit.chop_wood()
		self.assertEqual(unit.deliver_cargo(Wood, 5), 0)
		self.assertEqual(unit.moves_remaining, 25)


