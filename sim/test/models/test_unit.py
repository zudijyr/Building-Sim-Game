import unittest
from sim.geometry import *
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

class UnitModelTest(unittest.TestCase):

	def test_set_tile_map_raises_an_exception_if_a_non_TileMap_is_passed_in(self):
		u = DummyUnit()
		with self.assertRaises(UnitException) as error_context:
			u.set_tile_map("not a TileMap")
		self.assertEqual(error_context.exception.message, "tile_map must be an instance of TileMap")
		u.set_tile_map(TileMap(TileGrid(Size(10, 15))))

	def test_add_building_factory_adds_a_factory_to_the_units_building_factories(self):
		factory = Factory()
		factory.add_resource_requirement(DummyResource, 2)
		factory.set_product(DummyBuilding)
		u = DummyUnit()
		u.add_building_factory(factory)
		self.assertIs(u.building_factories[DummyBuilding.name], factory)

	def test_add_building_factory_raises_an_exception_if_a_factory_producting_that_kind_of_building_has_already_been_added(self):
		factory1 = Factory()
		factory1.add_resource_requirement(DummyResource, 2)
		factory1.set_product(DummyBuilding)
		factory2 = Factory()
		factory2.add_resource_requirement(DummyResource, 1)
		factory2.set_product(DummyBuilding)
		u = DummyUnit()

		u.add_building_factory(factory1)
		with self.assertRaises(UnitException) as error_context:
			u.add_building_factory(factory2)
		self.assertEqual(error_context.exception.message, "A factory for that building has already been added")

	def test_can_construct_building_returns_true_if_and_only_if_the_unit_is_carrying_the_resources_and_has_a_factory_that_can_produce_the_requested_building(self):
		u = DummyUnit()
		self.assertFalse(u.can_construct_building(DummyBuilding))

		factory = Factory()
		factory.add_resource_requirement(DummyResource, 2)
		factory.set_product(DummyBuilding)
		u.add_building_factory(factory)
		self.assertFalse(u.can_construct_building(DummyBuilding))

		u.receive_cargo(DummyResource, 2)
		self.assertTrue(u.can_construct_building(DummyBuilding))

	def test_construct_building_returns_a_new_instance_of_the_requested_building_if_the_unit_can_construct_it(self):
		u = DummyUnit()
		factory = Factory()
		factory.add_resource_requirement(DummyResource, 2)
		factory.set_product(DummyBuilding)
		u.add_building_factory(factory)
		u.receive_cargo(DummyResource, 2)
		self.assertIsInstance(u.construct_building(DummyBuilding), DummyBuilding)

	def test_act_pops_an_action_off_of_the_action_queue_and_calls_it_with_dt(self):
		output = []
		u = DummyUnit()
		u.action_queue.append(lambda dt: output.append(dt))
		u.act(11)
		self.assertEqual(len(output), 1)
		self.assertIn(11, output)

	def test_add_action_appends_a_function_to_the_action_queue_with_its_arguments_as_a_lambda_function(self):
		output = []
		action = lambda dt, *args, **kwargs: output.append({ 'dt':dt, 'args':args, 'kwargs':kwargs })
		u = DummyUnit()
		u.add_action(action, 'arg1', 'arg2', kwarg1='kwarg1', kwarg2='kwarg2')
		self.assertEqual(len(u.action_queue), 1)
		u.act(11)
		self.assertEqual(output, [ { 'dt': 11, 'args': ('arg1', 'arg2'), 'kwargs' : { 'kwarg1':'kwarg1', 'kwarg2':'kwarg2' } } ])

	def test_add_immediate_action_inserts_a_function_to_the_front_of_the_action_queue_with_its_arguments_as_a_lambda_function(self):
		output = []
		action = lambda dt, *args, **kwargs: output.append({ 'dt':dt, 'args':args, 'kwargs':kwargs })
		u = DummyUnit()
		u.add_action(action, 'arg1', 'arg2', kwarg1='kwarg1', kwarg2='kwarg2')
		u.add_immediate_action(action)
		self.assertEqual(len(u.action_queue), 2)
		u.act(12)
		self.assertEqual(output, [ { 'dt': 12, 'args': (), 'kwargs' : {} } ])
		self.assertEqual(len(u.action_queue), 1)

	def test_move_unit_toward_moves_the_unit_toward_the_target_point_as_far_as_the_unit_can_move_in_the_time_provided_and_appends_another_move_action_to_the_action_queue_if_it_does_not_fully_reach_the_destination(self):
		grid = TileGrid(Size(10, 15))
		tmap = TileMap(grid)
		u = DummyUnit()
		start_pt = Point(10, 10)
		tmap.place_unit(u, start_pt)
		target_pt = Point(20, 22)
		expected_movement_dist = (0.5 * tmap.tile_sz.diag)
		u.move_toward(1.0, target_pt)
		computed_unit_pt = tmap.get_unit_position(u)
		expected_unit_pt = start_pt + (target_pt - start_pt).u * expected_movement_dist
		# TODO: Add a method to point (is near)
		self.assertTrue(computed_unit_pt.near(expected_unit_pt))
		self.assertEqual(len(u.action_queue), 1)
		# TODO: Add test for terrain and terrain_improvement movement factors

	def test_move_unit_toward_moves_the_unit_toward_the_target_point_as_far_as_the_unit_can_move_in_the_time_provided_and_stops_the_movement_at_the_destination_if_it_could_move_farther_than_that(self):
		grid = TileGrid(Size(10, 15))
		tmap = TileMap(grid)
		u = DummyUnit()
		tmap.place_unit(u, Point(10, 10))
		u.move_toward(1.0, Point(12, 12))
		self.assertEqual(Point(12, 12), tmap.get_unit_position(u))
		self.assertEqual(len(u.action_queue), 0)

	def test_add_path_adds_a_move_action_to_the_action_queue_toward_the_specified_point(self):
		grid = TileGrid(Size(10, 15))
		tmap = TileMap(grid)
		u = DummyUnit()
		tmap.place_unit(u, Point(10, 10))
		u.add_path(Point(25, 10))
		u.act(1.0)
		unit_speed = tmap.tile_sz.diag * 0.5
		self.assertTrue(Point(10 + unit_speed, 10).near(tmap.get_unit_position(u)))
		self.assertEqual(len(u.action_queue), 1)
		u.act(1.0)
		self.assertTrue(Point(25, 10).near(tmap.get_unit_position(u)))
		self.assertEqual(len(u.action_queue), 0)

	def test_add_path_raises_an_exception_if_the_unit_has_not_yet_been_placed_on_a_map(self):
		u = DummyUnit()
		with self.assertRaises(UnitException) as error_context:
			u.add_path(Point(20, 22))
		self.assertEqual("This unit has not been placed on the tile map yet!", error_context.exception.message)

