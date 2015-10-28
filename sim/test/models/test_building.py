import unittest
from sim.models.building import *
from sim.models import resource

class BuildingModelTest(unittest.TestCase):

    def test_create_cabbage_farm(self):
        building = CabbageFarm(1, 1)
        self.assertEqual(building.input_cap, 5)

    def test_create_fishing_hole(self):
        building = FishingHole(5, 5)
        self.assertEqual(building.output_type, resource.Fish)
