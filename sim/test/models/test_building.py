import unittest
from sim.models.building import *
from sim.models import resource

class BuildingModelTest(unittest.TestCase):

    def test_create_cabbage_farm(self):
        building = CabbageFarm()
        self.assertEqual(building.input_cap, 5)

    def test_create_fishing_hole(self):
        building = FishingHole()
        self.assertEqual(building.output_type, resource.Fish)

    def test_produce_decreases_input_load_and_increases_output_load(self):
        building = Building()
        building.input_load = 5
        building.output_load = 1
        building.produce()
        building.produce()
        self.assertEqual(building.input_load, 3)
        self.assertEqual(building.output_load, 3)

    def test_produce_does_nothing_if_input_load_is_zero(self):
        building = Building()
        building.input_load = 0
        building.output_load = 0
        building.produce()
        self.assertEqual(building.input_load, 0)
        self.assertEqual(building.output_load, 0)

    def test_produce_does_nothing_if_output_load_is_at_output_cap(self):
        building = Building()
        building.input_load = 2
        building.output_load = 2
        building.output_cap = 2
        building.produce()
        self.assertEqual(building.input_load, 2)
        self.assertEqual(building.output_load, 2)

    def test_accept_input_raises_an_exception_if_input_load_is_at_input_cap(self):
        building = Building()
        building.input_load = 2
        building.input_cap = 2
        with self.assertRaises(BuildingException) as context:
            building.accept_input()
        self.assertIn('Building is already at input capacity', context.exception.message)

    def test_deliver_output_raises_an_exception_if_output_load_is_at_zero(self):
        building = Building()
        building.output_load = 0
        with self.assertRaises(BuildingException) as context:
            building.deliver_output()
        self.assertIn('Building has no output to deliver', context.exception.message)

