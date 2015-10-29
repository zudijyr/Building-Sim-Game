import unittest
from sim.models.building import *
from sim.models.resource import Fish, Wood, Cabbage, Stone

class BuildingModelTest(unittest.TestCase):

    def test_receive_cargo_accepts_cargo_of_a_specified_type(self):
        building = Building()
        building.container.add_resource_slot(Fish, 10)
        self.assertEqual(building.receive_cargo(Fish, 5), 0)
        self.assertEqual(building.container.current_load(Fish), 5)
        self.assertEqual(building.container.remaining_capacity(Fish), 5)

    def test_receive_cargo_accepts_as_much_cargo_as_its_capacity_allows_and_returns_the_rest(self):
        building = Building()
        building.container.add_resource_slot(Fish, 10)
        building.container.load_cargo(Fish, 7)
        self.assertEqual(building.receive_cargo(Fish, 5), 2)
        self.assertEqual(building.container.current_load(Fish), 10)
        self.assertEqual(building.container.remaining_capacity(Fish), 0)

    def test_deliver_cargo_gives_up_cargo_of_a_specified_type(self):
        building = Building()
        building.container.add_resource_slot(Fish, 10)
        building.container.load_cargo(Fish, 7)
        self.assertEqual(building.deliver_cargo(Fish, 5), 5)
        self.assertEqual(building.container.current_load(Fish), 2)
        self.assertEqual(building.container.remaining_capacity(Fish), 8)

    def test_deliver_cargo_gives_up_as_much_cargo_of_a_specified_type_as_it_currently_holds(self):
        building = Building()
        building.container.add_resource_slot(Fish, 10)
        building.container.load_cargo(Fish, 3)
        self.assertEqual(building.deliver_cargo(Fish, 5), 3)
        self.assertEqual(building.container.current_load(Fish), 0)
        self.assertEqual(building.container.remaining_capacity(Fish), 10)

    def test_operate_digests_resources_with_all_the_available_digesters(self):
        building = Building()

        building.container.add_resource_slot(Fish, 10)
        building.container.add_resource_slot(Wood, 10)
        building.container.add_resource_slot(Cabbage, 10)
        building.container.add_resource_slot(Stone, 10)

        building.container.load_cargo(Fish, 10)
        building.container.load_cargo(Wood, 10)

        cabbage_producer = ProducerConsumer()
        cabbage_producer.add_resource_requirement(Fish, 3)
        cabbage_producer.add_resource_requirement(Wood, 2)
        cabbage_producer.add_resource_product(Cabbage, 2)
        building.digesters.append(cabbage_producer)

        stone_producer = ProducerConsumer()
        stone_producer.add_resource_requirement(Fish, 1)
        stone_producer.add_resource_requirement(Wood, 3)
        stone_producer.add_resource_requirement(Cabbage, 5)
        stone_producer.add_resource_product(Stone, 1)
        building.digesters.append(stone_producer)

        building.operate()
        self.assertEqual(building.container.current_load(Fish), 7)
        self.assertEqual(building.container.current_load(Wood), 8)
        self.assertEqual(building.container.current_load(Cabbage), 2)
        self.assertEqual(building.container.current_load(Stone), 0)

        building.operate()
        self.assertEqual(building.container.current_load(Fish), 4)
        self.assertEqual(building.container.current_load(Wood), 6)
        self.assertEqual(building.container.current_load(Cabbage), 4)
        self.assertEqual(building.container.current_load(Stone), 0)

        building.operate()
        self.assertEqual(building.container.current_load(Fish), 0)
        self.assertEqual(building.container.current_load(Wood), 1)
        self.assertEqual(building.container.current_load(Cabbage), 1)
        self.assertEqual(building.container.current_load(Stone), 1)

