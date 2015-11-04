import unittest
from sim.models.building import Building
from sim.models.resource import Fish, Wood, Cabbage, Stone
from sim.models.producer_consumer import ResourcePlant

class BuildingModelTest(unittest.TestCase):

    def test_produce_resources_digests_resources_with_all_the_available_digesters(self):
        building = Building()

        building.container.add_resource_slot(Fish, 10)
        building.container.add_resource_slot(Wood, 10)
        building.container.add_resource_slot(Cabbage, 10)
        building.container.add_resource_slot(Stone, 10)

        building.receive_cargo(Fish, 10)
        building.receive_cargo(Wood, 10)

        cabbage_plant = ResourcePlant()
        cabbage_plant.add_resource_requirement(Fish, 3)
        cabbage_plant.add_resource_requirement(Wood, 2)
        cabbage_plant.add_resource_product(Cabbage, 2)
        building.add_resource_plant(cabbage_plant)

        stone_plant = ResourcePlant()
        stone_plant.add_resource_requirement(Fish, 1)
        stone_plant.add_resource_requirement(Wood, 3)
        stone_plant.add_resource_requirement(Cabbage, 5)
        stone_plant.add_resource_product(Stone, 1)
        building.add_resource_plant(stone_plant)

        building.produce_resources()
        self.assertEqual(building.container.current_load(Fish), 7)
        self.assertEqual(building.container.current_load(Wood), 8)
        self.assertEqual(building.container.current_load(Cabbage), 2)
        self.assertEqual(building.container.current_load(Stone), 0)

        building.produce_resources()
        self.assertEqual(building.container.current_load(Fish), 4)
        self.assertEqual(building.container.current_load(Wood), 6)
        self.assertEqual(building.container.current_load(Cabbage), 4)
        self.assertEqual(building.container.current_load(Stone), 0)

        building.produce_resources()
        self.assertEqual(building.container.current_load(Fish), 0)
        self.assertEqual(building.container.current_load(Wood), 1)
        self.assertEqual(building.container.current_load(Cabbage), 1)
        self.assertEqual(building.container.current_load(Stone), 1)


