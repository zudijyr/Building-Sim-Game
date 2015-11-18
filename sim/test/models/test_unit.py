import unittest
from unittest.mock import MagicMock

from sim.geometry import *
from sim.models.unit import Unit, UnitException
from sim.models.producer_consumer import Factory
from sim.models.building import Building
from sim.models.resource import Resource
from sim.models.tile_map import TileMap
from sim.models.tile_grid import TileGrid
from sim.models.terrain import Plains
from sim.models.terrain_improvement import Road
from sim.models.action import Action

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

	def test_construct_building_raises_an_exception_if_the_unit_cannot_build_that_type_of_building(self):
		u = DummyUnit()
		with self.assertRaises(UnitException) as error_context:
			u.construct_building(DummyBuilding)
		self.assertEqual("This unit cannot build that building", error_context.exception.message)

	def test_act_pops_an_action_off_of_the_action_queue_and_executes_it_and_if_it_is_not_complete_puts_it_back_to_the_front_of_the_action_queue(self):
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

	def test_act_pops_an_action_off_of_the_action_queue_and_executes_it_and_if_it_is_complete_executes_the_finish_method(self):
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

	def test_act_pops_an_action_off_of_the_action_queue_and_if_it_is_not_possible_returns_immediately(self):
		action = Action()
		action.is_possible = MagicMock(return_value=False)
		action.execute = MagicMock()
		u = DummyUnit()
		u.add_action(action)
		u.act(1.0)
		action.is_possible.assert_called_once_with(u, 1.0)
		action.execute.assert_not_called()
		self.assertEqual(len(u.action_queue), 0)

