import unittest
from sim.models.building import *
from sim.models.resource import *

class BuildingModelTest(unittest.TestCase):

    def test_operate_digests_resources_with_all_the_available_digesters(self):
        building = Building()

        building.container.add_resource_slot(Fish, 10)
        building.container.add_resource_slot(Wood, 10)
        building.container.add_resource_slot(Cabbage, 10)
        building.container.add_resource_slot(Stone, 10)

        building.receive_cargo(Fish, 10)
        building.receive_cargo(Wood, 10)

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

class CabbageFarmModelTest(unittest.TestCase):

    def test_cabbage_farm_produces_cabbage_from_wood(self):
        farm = CabbageFarm()
        farm.receive_cargo(Wood, 3)
        farm.operate()
        farm.operate()
        self.assertEqual(farm.deliver_cargo(Cabbage, 10), 2)

class DockModelTest(unittest.TestCase):

    def test_dock_produces_fish(self):
        dock = Dock()
        dock.operate()
        dock.operate()
        self.assertEqual(dock.deliver_cargo(Fish, 10), 2)

class FishingHoleModelTest(unittest.TestCase):

    def test_fishing_hole_produces_fish(self):
        hole = FishingHole()
        hole.operate()
        hole.operate()
        self.assertEqual(hole.deliver_cargo(Fish, 10), 6)


