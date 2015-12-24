import unittest
from unittest.mock import MagicMock

from sim.geometry import Point, Size, Vector
from sim.models.unit import Unit, UnitException
from sim.models.producer_consumer import Factory
from sim.models.building import Building
from sim.models.resource import Resource
from sim.models.tile_map import TileMap
from sim.models.tile_grid import TileGrid
from sim.models.terrain import TerrainType, Water
from sim.models.actions import Action


class DummyUnit(Unit):
	name = 'Dummy Unit'
	strength = 10
	movement_speed = 0.5

	def __init__(self):
		super().__init__()
		self.traversable_terrain_types.add(TerrainType.land)


class DummyBuilding(Building):
	name = 'Dummy Building'


class DummyResource(Resource):
	name = 'Dummy Resource'
	weight = 1


class UnitModelTest(unittest.TestCase):

	def test_add_building_factory_adds_a_factory_to_the_units_building_factories(self):  # noqa
		factory = Factory()
		factory.add_resource_requirement(DummyResource, 2)
		factory.set_product(DummyBuilding)
		u = DummyUnit()
		u.add_building_factory(factory)
		self.assertIs(u.building_factories[DummyBuilding.name], factory)

	def test_add_building_factory_raises_an_exception_if_a_factory_producting_that_kind_of_building_has_already_been_added(self):  # noqa
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
		self.assertEqual(
			error_context.exception.message,
			"A factory for that building has already been added",
			)

	def test_can_construct_building_returns_true_if_and_only_if_the_unit_is_carrying_the_resources_and_has_a_factory_that_can_produce_the_requested_building_and_the_unit_is_placed_on_the_map(self):  # noqa
		tmap = TileMap(TileGrid(Size(10, 10)))
		u = DummyUnit()
		tmap.place_unit(u, Point(0, 0))
		self.assertFalse(u.can_construct_building(DummyBuilding))

		factory = Factory()
		factory.add_resource_requirement(DummyResource, 2)
		factory.set_product(DummyBuilding)
		u.add_building_factory(factory)
		self.assertFalse(u.can_construct_building(DummyBuilding))

		u.receive_cargo(DummyResource, 2)
		self.assertTrue(u.can_construct_building(DummyBuilding))

	def test_construct_building_returns_a_new_instance_of_the_requested_building_if_the_unit_can_construct_it(self):  # noqa
		u = DummyUnit()
		factory = Factory()
		factory.add_resource_requirement(DummyResource, 2)
		factory.set_product(DummyBuilding)
		u.add_building_factory(factory)
		u.receive_cargo(DummyResource, 2)
		self.assertIsInstance(
			u.construct_building(DummyBuilding),
			DummyBuilding,
			)

	def test_construct_building_raises_an_exception_if_the_unit_cannot_build_that_type_of_building(self):  # noqa
		u = DummyUnit()
		with self.assertRaises(UnitException) as error_context:
			u.construct_building(DummyBuilding)
		self.assertEqual(
			"This unit cannot build that building",
			error_context.exception.message,
			)

	def test_act_pops_an_action_off_of_the_action_queue_and_executes_it_and_if_it_is_not_complete_puts_it_back_to_the_front_of_the_action_queue(self):  # noqa
		action = Action()
		action.is_possible = MagicMock(return_value=True)
		action.execute = MagicMock()
		action.is_complete = MagicMock(return_value=False)
		action.finish = MagicMock()
		u = DummyUnit()
		u.add_action(action)
		u.act(1.0)
		action.is_possible.assert_called_once_with(u, 1.0)
		action.execute.assert_called_once_with(u, 1.0)
		action.is_complete.assert_called_once_with(u, 1.0)
		action.finish.assert_not_called()
		self.assertEqual(len(u.action_queue), 1)

	def test_act_pops_an_action_off_of_the_action_queue_and_executes_it_and_if_it_is_complete_executes_the_finish_method(self):  # noqa
		action = Action()
		action.is_possible = MagicMock(return_value=True)
		action.execute = MagicMock()
		action.is_complete = MagicMock(return_value=True)
		action.finish = MagicMock()
		u = DummyUnit()
		u.add_action(action)
		u.act(1.0)
		action.is_possible.assert_called_once_with(u, 1.0)
		action.execute.assert_called_once_with(u, 1.0)
		action.is_complete.assert_called_once_with(u, 1.0)
		action.finish.assert_called_once_with(u, 1.0)
		self.assertEqual(len(u.action_queue), 0)

	def test_act_pops_an_action_off_of_the_action_queue_and_if_it_is_not_possible_returns_immediately(self):  # noqa
		action = Action()
		action.is_possible = MagicMock(return_value=False)
		action.execute = MagicMock()
		u = DummyUnit()
		u.add_action(action)
		u.act(1.0)
		action.is_possible.assert_called_once_with(u, 1.0)
		action.execute.assert_not_called()
		self.assertEqual(len(u.action_queue), 0)

	def test_move_moves_a_unit_along_a_movement_vector(self):
		tmap = TileMap(TileGrid(Size(10, 10)))
		u = DummyUnit()
		tmap.place_unit(u, Point(55, 75))
		u.move(Vector(-5, 10))
		self.assertEqual(u.pt, Point(50, 85))

	def test_move_raises_an_exception_if_the_unit_has_not_yet_been_placed_on_the_map(self):  # noqa
		u = DummyUnit()
		with self.assertRaises(UnitException) as error_context:
			u.move(Vector(-5, -10))
		self.assertIn(
			"not yet placed on the map",
			error_context.exception.message,
			)

	def test_move_raises_an_exception_if_the_move_would_take_the_unit_out_of_bounds(self):  # noqa
		tmap = TileMap(TileGrid(Size(10, 10)))
		u = DummyUnit()
		tmap.place_unit(u, Point(5, 5))
		with self.assertRaises(UnitException) as error_context:
			u.move(Vector(-5, -10))
		self.assertIn("out of bounds", error_context.exception.message)

	def test_move_raises_an_exception_if_the_move_would_take_the_unit_into_non_traversable_terrain(self):  # noqa
		tmap = TileMap(TileGrid(Size(10, 10)))
		u = DummyUnit()
		tmap.place_unit(u, Point(5, 5))
		tmap.get_tile(Point(15, 5)).set_terrain(Water)
		with self.assertRaises(UnitException) as error_context:
			u.move(Vector(10, 0))
		self.assertIn("unit cannot traverse", error_context.exception.message)

	def test_tile_returns_the_tile_at_the_units_position(self):
		tmap = TileMap(TileGrid(Size(10, 10)))
		u = DummyUnit()
		tmap.place_unit(u, Point(110, 110))
		tile = tmap.tile_grid.get_tile(Point(5, 5))
		tile.tile_id = "target tile"
		self.assertEqual(u.tile.tile_id, "target tile")
