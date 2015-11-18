import unittest
from sim.geometry import *
from sim.models.action import *
from sim.models.unit import Unit, UnitException
from sim.models.producer_consumer import Factory
from sim.models.building import Building
from sim.models.resource import Resource
from sim.models.tile_map import TileMap
from sim.models.tile_grid import TileGrid
from sim.models.terrain import Plains
from sim.models.terrain_improvement import Road

class DummyUnit(Unit):
	name = 'Dummy Unit'
	strength = 10
	movement_speed = 0.5

class DummyBuilding(Building):
	name = 'Dummy Building'

class DummyResource(Resource):
	name = 'Dummy Resource'
	weight = 1

class ActionTest(unittest.TestCase):

	def test_move_toward__is_possible_returns_true_if_and_only_if_the_unit_has_been_placed_on_the_map(self):
		tmap = TileMap(TileGrid(Size(10, 15)))
		u = DummyUnit()
		move_action = MoveToward(Point(20, 22))
		self.assertFalse(move_action.is_possible(u, 1.0))
		tmap.place_unit(u, Point(10, 10))
		self.assertTrue(move_action.is_possible(u, 1.0))

	#    grid = TileGrid(Size(10, 15))
	#    tmap = TileMap(grid)
	#    u = DummyUnit()
	#    start_pt = Point(10, 10)
	#    tmap.place_unit(u, start_pt)
	#    target_pt = Point(20, 22)
	#    expected_movement_dist = (0.5 * tmap.tile_sz.diag)
	#    u.move_toward(1.0, target_pt)
	#    computed_unit_pt = tmap.get_unit_position(u)
	#    expected_unit_pt = start_pt + (target_pt - start_pt).u * expected_movement_dist
	#    # TODO: Add a method to point (is near)
	#    self.assertTrue(computed_unit_pt.near(expected_unit_pt))
	#    self.assertEqual(len(u.action_queue), 1)
	#    # TODO: Add test for terrain and terrain_improvement movement factors

	#def test_move_unit_toward_moves_the_unit_toward_the_target_point_as_far_as_the_unit_can_move_in_the_time_provided_and_stops_the_movement_at_the_destination_if_it_could_move_farther_than_that(self):
	#    grid = TileGrid(Size(10, 15))
	#    tmap = TileMap(grid)
	#    u = DummyUnit()
	#    tmap.place_unit(u, Point(10, 10))
	#    u.move_toward(1.0, Point(12, 12))
	#    self.assertEqual(Point(12, 12), tmap.get_unit_position(u))
	#    self.assertEqual(len(u.action_queue), 0)

	#def test_add_path_adds_a_move_action_to_the_action_queue_toward_the_specified_point(self):
	#    grid = TileGrid(Size(10, 15))
	#    tmap = TileMap(grid)
	#    u = DummyUnit()
	#    tmap.place_unit(u, Point(10, 10))
	#    u.add_path(Point(25, 10))
	#    u.act(1.0)
	#    unit_speed = tmap.tile_sz.diag * 0.5
	#    self.assertTrue(Point(10 + unit_speed, 10).near(tmap.get_unit_position(u)))
	#    self.assertEqual(len(u.action_queue), 1)
	#    u.act(1.0)
	#    self.assertTrue(Point(25, 10).near(tmap.get_unit_position(u)))
	#    self.assertEqual(len(u.action_queue), 0)

	#def test_add_path_raises_an_exception_if_the_unit_has_not_yet_been_placed_on_a_map(self):
	#    u = DummyUnit()
	#    with self.assertRaises(UnitException) as error_context:
	#        u.add_path(Point(20, 22))
	#    self.assertEqual("This unit has not been placed on the tile map yet!", error_context.exception.message)

