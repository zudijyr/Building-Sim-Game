import unittest
from sim.models.resource import Fish
from sim.models.cargo_container import CargoContainer, CargoContainerException

class CargoContainerModelTest(unittest.TestCase):

    def test_add_resource_slot_creates_a_new_slot_for_a_specified_resource(self):
        bag = CargoContainer()
        bag.add_resource_slot(Fish, 10)
        self.assertIn(Fish.name, bag.cargo_slots.keys())
        self.assertEqual(bag.cargo_slots[Fish.name]['capacity'], 10)
        self.assertEqual(bag.cargo_slots[Fish.name]['load'], 0)
        self.assertIs(bag.cargo_slots[Fish.name]['type'], Fish)

    def test_add_resource_slot_raises_error_if_there_is_already_a_slot_for_that_resource_type(self):
        bag = CargoContainer()
        bag.add_resource_slot(Fish, 10)
        with self.assertRaises(CargoContainerException) as error_context:
            bag.add_resource_slot(Fish, 12)
        self.assertIn("An input slot of that resource type has already been added", error_context.exception.message)

    def test_can_load_cargo_returns_true_if_slot_is_not_at_capacity(self):
        bag = CargoContainer()
        bag.add_resource_slot(Fish, 1)
        self.assertTrue(bag.can_load_cargo(Fish, 1))

    def test_can_load_cargo_returns_false_if_slot_is_at_capacity(self):
        bag = CargoContainer()
        bag.add_resource_slot(Fish, 0)
        self.assertFalse(bag.can_load_cargo(Fish, 1))

    def test_can_load_cargo_returns_false_if_slot_for_that_resource_is_not_yet_added(self):
        bag = CargoContainer()
        self.assertFalse(bag.can_load_cargo(Fish, 1))

    def test_can_unload_cargo_returns_true_if_slot_has_a_load(self):
        bag = CargoContainer()
        bag.add_resource_slot(Fish, 1)
        bag.cargo_slots[Fish.name]['load'] = 1
        self.assertTrue(bag.can_unload_cargo(Fish, 1))

    def test_can_unload_cargo_returns_false_if_slot_has_no_load(self):
        bag = CargoContainer()
        bag.add_resource_slot(Fish, 1)
        self.assertFalse(bag.can_unload_cargo(Fish, 1))

    def test_can_unload_cargo_returns_false_if_slot_for_that_resource_is_not_yet_added(self):
        bag = CargoContainer()
        self.assertFalse(bag.can_unload_cargo(Fish, 1))

    def test_load_cargo_increases_load_of_slot_if_bag_can_load_the_resource(self):
        bag = CargoContainer()
        bag.add_resource_slot(Fish, 1)
        bag.load_cargo(Fish, 1)
        self.assertEqual(bag.cargo_slots[Fish.name]['load'], 1)

    def test_load_cargo_raises_exception_if_bag_cannot_load_the_resource(self):
        bag = CargoContainer()
        with self.assertRaises(CargoContainerException) as error_context:
            bag.load_cargo(Fish, 1)
        self.assertIn("Cannot load resource", error_context.exception.message)

    def test_unload_cargo_decreases_load_of_slot_if_bag_can_unload_the_resource(self):
        bag = CargoContainer()
        bag.add_resource_slot(Fish, 1)
        bag.cargo_slots[Fish.name]['load'] = 1
        bag.unload_cargo(Fish, 1)
        self.assertEqual(bag.cargo_slots[Fish.name]['load'], 0)

    def test_unload_cargo_raises_exception_if_bag_cannot_unload_the_resource(self):
        bag = CargoContainer()
        with self.assertRaises(CargoContainerException) as error_context:
            bag.unload_cargo(Fish, 1)
        self.assertIn("Cannot unload resource", error_context.exception.message)

