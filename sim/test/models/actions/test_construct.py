import unittest
from unittest.mock import MagicMock

from sim.models.actions.construct import Construct


class ConstructTest(unittest.TestCase):

	def test_is_possible_returns_false_if_unit_can_not_construct_that_building_type(self):  # noqa
		dummy_building = MagicMock()
		dummy_unit = MagicMock()
		dummy_unit.can_construct_building.return_value = False
		construct = Construct(dummy_building)
		self.assertFalse(construct.is_possible(dummy_unit, 1.0))
		dummy_unit.can_construct_building.assert_called_once_with(
			dummy_building
			)
		dummy_unit.can_construct_building.return_value = True
		self.assertTrue(construct.is_possible(dummy_unit, 1.0))

	def test_is_complete_returns_true_if_and_only_if_the_elapsed_time_is_greater_than_or_equal_to_the_buildings_build_time(self):  # noqa
		dummy_building = MagicMock()
		dummy_building.build_time = 2.0
		dummy_unit = MagicMock()
		construct = Construct(dummy_building)
		construct.elapsed_time = 1.9
		self.assertFalse(construct.is_complete(dummy_unit, 1.0))
		construct.elapsed_time = 2.0
		self.assertTrue(construct.is_complete(dummy_unit, 1.0))

	def test_finish_constructs_the_building_and_places_it_on_the_tile_map(self):  # noqa
		dummy_building = MagicMock()
		dummy_unit = MagicMock()
		dummy_unit.pt = 'dummy_point'
		dummy_unit.construct_building.return_value = dummy_building
		construct = Construct(dummy_building)
		construct.finish(dummy_unit, 1.0)
		dummy_unit.construct_building.assert_called_once_with(dummy_building)
		dummy_unit.tile_map.place_building.assert_called_once_with(
			dummy_building,
			'dummy_point',
			)

	def test_seconds_remaining_property_returns_the_difference_between_the_elapsed_time_and_the_build_time(self):  # noqa
		dummy_building = MagicMock()
		dummy_building.build_time = 2.0
		construct = Construct(dummy_building)
		construct.elapsed_time = 1.9
		self.assertEqual(round(construct.seconds_remaining, 6), 0.1)

#    def test_move_toward__is_possible_returns_true_if_and_only_if_the_unit_has_been_placed_on_the_map(self):  # noqa
#        tmap = TileMap(TileGrid(Size(10, 15)))
#        u = DummyUnit()
#        move_action = MoveToward(Point(20, 22))
#        self.assertFalse(move_action.is_possible(u, 1.0))
#        tmap.place_unit(u, Point(10, 10))
#        self.assertTrue(move_action.is_possible(u, 1.0))
#
#    def test_move_toward__is_complete_returns_true_if_and_only_if_the_unit_is_near_the_destination_point(self):  # noqa
#        tmap = TileMap(TileGrid(Size(10, 15)))
#        u = DummyUnit()
#        tmap.place_unit(u, Point(0, 0))
#        move_action = MoveToward(Point(20, 22))
#        self.assertFalse(move_action.is_complete(u, 1.0))
#        tmap.set_unit_position(u, Point(20 + EPS/2, 22))
#        self.assertTrue(move_action.is_complete(u, 1.0))

	#    grid = TileGrid(Size(10, 15))
	#    tmap = TileMap(grid)
	#    u = DummyUnit()
	#    start_pt = Point(10, 10)
	#    tmap.place_unit(u, start_pt)
	#    target_pt = Point(20, 22)
	#    expected_movement_dist = (0.5 * tmap.tile_sz.diag)
	#    u.move_toward(1.0, target_pt)
	#    computed_unit_pt = tmap.get_unit_position(u)
	#    expected_unit_pt = (start_pt + (target_pt - start_pt).u *
	#                        expected_movement_dist)
	#    # TODO: Add a method to point (is near)
	#    self.assertTrue(computed_unit_pt.near(expected_unit_pt))
	#    self.assertEqual(len(u.action_queue), 1)
	#    # TODO: Add test for terrain and terrain_improvement movement factors

	# def test_move_unit_toward_moves_the_unit_toward_the_target_point_as_far_as_the_unit_can_move_in_the_time_provided_and_stops_the_movement_at_the_destination_if_it_could_move_farther_than_that(self):  # noqa
	#     grid = TileGrid(Size(10, 15))
	#     tmap = TileMap(grid)
	#     u = DummyUnit()
	#     tmap.place_unit(u, Point(10, 10))
	#     u.move_toward(1.0, Point(12, 12))
	#     self.assertEqual(Point(12, 12), tmap.get_unit_position(u))
	#     self.assertEqual(len(u.action_queue), 0)

	# def test_add_path_adds_a_move_action_to_the_action_queue_toward_the_specified_point(self):  # noqa
	#     grid = TileGrid(Size(10, 15))
	#     tmap = TileMap(grid)
	#     u = DummyUnit()
	#     tmap.place_unit(u, Point(10, 10))
	#     u.add_path(Point(25, 10))
	#     u.act(1.0)
	#     unit_speed = tmap.tile_sz.diag * 0.5
	#     self.assertTrue(
	#         Point(10 + unit_speed, 10).near(tmap.get_unit_position(u))
	#         )
	#     self.assertEqual(len(u.action_queue), 1)
	#     u.act(1.0)
	#     self.assertTrue(Point(25, 10).near(tmap.get_unit_position(u)))
	#     self.assertEqual(len(u.action_queue), 0)

	# def test_add_path_raises_an_exception_if_the_unit_has_not_yet_been_placed_on_a_map(self):  # noqa
	#     u = DummyUnit()
	#     with self.assertRaises(UnitException) as error_context:
	#         u.add_path(Point(20, 22))
	#     self.assertEqual(
	#         "This unit has not been placed on the tile map yet!",
	#         error_context.exception.message,
	#         )
