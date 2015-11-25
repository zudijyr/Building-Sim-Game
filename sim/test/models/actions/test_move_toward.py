import unittest
from unittest.mock import MagicMock, patch

from sim.models.actions import Action, ActionException
from sim.models.actions.move_toward import MoveToward
from sim.geometry import *

class MoveTowardTest(unittest.TestCase):

	def test_is_possible_returns_false_if_unit_has_not_been_placed_on_the_map(self):
		dummy_unit = MagicMock()
		dummy_unit.tile_map = None
		movement = MoveToward(Point(3, 4))
		self.assertFalse(movement.is_possible(dummy_unit, 1.0))

	def test_is_possible_returns_false_if_unit_is_at_or_very_near_the_target_point(self):
		dummy_unit = MagicMock()
		dummy_unit.pt = Point(3 + EPS/2, 4)
		movement = MoveToward(Point(3, 4))
		self.assertFalse(movement.is_possible(dummy_unit, 1.0))

	def test_is_possible_returns_true_if_the_unit_can_move_toward_the_point(self):
		dummy_unit = MagicMock()
		dummy_unit.pt = Point(0, 0)
		movement = MoveToward(Point(3, 4))
		self.assertTrue(movement.is_possible(dummy_unit, 1.0))

	def test__execute_moves_the_unit_toward_the_target_point_facoring_in_terrain_and_movement_speed(self):
		dummy_tile = MagicMock()
		dummy_tile.terrain.movement_factor = 0.5
		dummy_tile.terrain_improvement.movement_factor = 0.25
		dummy_unit = MagicMock()
		dummy_unit.pt = Point(1, 2)
		dummy_unit.tile = dummy_tile
		dummy_unit.movement_speed = 3
		dummy_unit.tile_map.tile_sz.diag = 7
		movement = MoveToward(Point(3, 4))
		movement._execute(dummy_unit, 2.0)
		dummy_unit.move.assert_called_once_with(Vector(2, 2).u*min(3*0.5*0.25*7*2.0,Vector(2, 2).M))

	def test_is_complete_returns_true_if_and_only_if_unit_is_at_or_very_near_the_target_point(self):
		dummy_unit = MagicMock()
		dummy_unit.pt = Point(3 + EPS/2, 4)
		movement = MoveToward(Point(0, 0))
		self.assertFalse(movement.is_complete(dummy_unit, 1.0))
		movement = MoveToward(Point(3, 4))
		self.assertTrue(movement.is_complete(dummy_unit, 1.0))

