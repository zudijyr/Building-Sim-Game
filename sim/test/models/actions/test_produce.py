import unittest
from unittest.mock import MagicMock

from sim.models.actions.produce import Produce
from sim.models.building import Building, BuildingException
from sim.models.resource import Fish, Wood, Cabbage, Stone
from sim.models.producer_consumer import ProducerConsumer, ResourcePlant

class DummyProducerConsumer(ProducerConsumer):

	def digest(self):
		pass

class DeliverTest(unittest.TestCase):

	def test_is_possible_returns_false_if_the_building_has_no_remaining_capacity_of_the_resource(self):
		building = Building()

		building.container.add_resource_slot(Fish, 10)
		building.container.add_resource_slot(Cabbage, 10)
		building.container.add_resource_slot(Stone, 10)

		building.receive_cargo(Fish, 10)

		cabbage_plant = ResourcePlant()
		cabbage_plant.add_resource_requirement(Fish, 3)
		cabbage_plant.add_resource_product(Cabbage, 2)
		building.add_resource_plant(cabbage_plant)

		produce = Produce(building, Cabbage, 1)
		self.assertFalse(produce.is_possible(building, 1))

	def test__execute_produces_resource_based_on_the_transfer_rate_and_dt(self):
		building = Building()

		building.container.add_resource_slot(Fish, 10)
		building.container.add_resource_slot(Cabbage, 10)
		building.container.add_resource_slot(Stone, 10)

		building.receive_cargo(Fish, 10)

		cabbage_plant = ResourcePlant()
		cabbage_plant.add_resource_requirement(Fish, 3)
		cabbage_plant.add_resource_product(Cabbage, 2)
		building.add_resource_plant(cabbage_plant)

		produce = Produce(building, Cabbage, 1)
		self.assertTrue(produce.is_possible(building, 1))
		produce._execute(building, 2)
		self.assertEqual(building.container.current_load(Cabbage), 2)
