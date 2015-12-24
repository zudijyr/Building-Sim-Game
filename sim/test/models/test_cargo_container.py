import unittest
from sim.models.resource import Fish, Cabbage, Wood
from sim.models.cargo_container import MixedCargoContainer
from sim.models.cargo_container import SlottedCargoContainer
from sim.models.cargo_container import CargoContainerException


class MixedCargoContainerModelTest(unittest.TestCase):

	def test_set_weight_capacity_raises_an_exception_if_the_requested_capacity_is_less_than_or_equal_to_zero(self):  # noqa
		bag = MixedCargoContainer()
		with self.assertRaises(CargoContainerException) as error_context:
			bag.set_weight_capacity(0)
		self.assertEqual(
			"Weight capacity must be greater than 0",
			error_context.exception.message,
			)

	def test_set_weight_capacity_raises_an_exception_if_the_requested_capacity_is_less_than_or_equal_to_the_current_weight_in_the_container(self):  # noqa
		bag = MixedCargoContainer()
		bag.set_weight_capacity(Fish.weight * 3)
		slot = bag.get_slot(Fish)
		slot['load'] = 3
		with self.assertRaises(CargoContainerException) as error_context:
			bag.set_weight_capacity(Fish.weight * 2)
		self.assertIn(
			"Capacity must be greater than or equal to the current weight",
			error_context.exception.message,
			)

	def test_get_current_weight_computes_the_total_weight_of_all_resource_items_in_the_container(self):  # noqa
		bag = MixedCargoContainer()
		bag.set_weight_capacity(100)
		slot = bag.get_slot(Fish)
		slot['load'] = 3
		slot = bag.get_slot(Cabbage)
		slot['load'] = 5
		self.assertEqual(
			bag.get_current_weight(),
			3 * Fish.weight + 5 * Cabbage.weight,
			)

	def test_remaining_capacity_computes_the_number_of_resource_type_that_can_still_be_held_in_the_container(self):  # noqa
		bag = MixedCargoContainer()
		bag.set_weight_capacity(100)
		slot = bag.get_slot(Fish)
		slot['load'] = 3
		slot = bag.get_slot(Cabbage)
		slot['load'] = 5
		self.assertEqual(
			bag.remaining_capacity(Wood),
			(100 - 3 * Fish.weight - 5 * Cabbage.weight) // Wood.weight,
			)

	def test_current_load_returns_the_current_number_of_resource_type_held_in_the_container(self):  # noqa
		bag = MixedCargoContainer()
		bag.set_weight_capacity(100)
		slot = bag.get_slot(Fish)
		slot['load'] = 3
		slot = bag.get_slot(Cabbage)
		slot['load'] = 5
		self.assertEqual(bag.current_load(Fish), 3)

	def test_load_cargo_increases_load_of_container(self):
		bag = MixedCargoContainer()
		bag.set_weight_capacity(Fish.weight * 10)
		remains = bag.load_cargo(Fish, 1)
		self.assertEqual(bag.current_load(Fish), 1)
		self.assertEqual(remains, 0)

	def test_load_cargo_increases_load_of_slot_if_bag_can_hold_the_resource_and_returns_excess_that_could_not_be_loaded(self):  # noqa
		bag = MixedCargoContainer()
		bag.set_weight_capacity(Fish.weight * 5 - 1)
		remains = bag.load_cargo(Fish, 7)
		self.assertEqual(bag.current_load(Fish), 4)
		self.assertEqual(remains, 3)

	def test_load_cargo_returns_entire_load_if_slot_is_already_at_capacity(self):  # noqa
		bag = MixedCargoContainer()
		bag.set_weight_capacity(Fish.weight * 3)
		bag.get_slot(Fish)['load'] = 3
		remains = bag.load_cargo(Fish, 7)
		self.assertEqual(bag.current_load(Fish), 3)
		self.assertEqual(remains, 7)

	def test_unload_cargo_decreases_load_of_container(self):
		bag = MixedCargoContainer()
		bag.set_weight_capacity(Fish.weight * 10)
		bag.get_slot(Fish)['load'] = 1
		load = bag.unload_cargo(Fish, 1)
		self.assertEqual(bag.current_load(Fish), 0)
		self.assertEqual(load, 1)

	def test_unload_cargo_decreases_load_of_container_and_returns_all_available_cargo_up_to_the_requested_quantity(self):  # noqa
		bag = MixedCargoContainer()
		bag.set_weight_capacity(Fish.weight * 10)
		bag.get_slot(Fish)['load'] = 3
		load = bag.unload_cargo(Fish, 7)
		self.assertEqual(bag.current_load(Fish), 0)
		self.assertEqual(load, 3)

	def test_unload_cargo_returns_nothing_if_bag_has_no_resources_of_requested_type(self):  # noqa
		bag = MixedCargoContainer()
		bag.set_weight_capacity(Fish.weight * 10)
		load = bag.unload_cargo(Fish, 7)
		self.assertEqual(bag.current_load(Fish), 0)
		self.assertEqual(load, 0)


class SlottedCargoContainerModelTest(unittest.TestCase):

	def test_add_resource_slot_creates_a_new_slot_for_a_specified_resource(self):  # noqa
		tray = SlottedCargoContainer()
		tray.add_resource_slot(Fish, 10)
		self.assertIn(Fish.name, tray.cargo_slots.keys())
		self.assertEqual(tray.cargo_slots[Fish.name]['capacity'], 10)
		self.assertEqual(tray.cargo_slots[Fish.name]['load'], 0)
		self.assertIs(tray.cargo_slots[Fish.name]['type'], Fish)

	def test_add_resource_slot_raises_error_if_there_is_already_a_slot_for_that_resource_type(self):  # noqa
		tray = SlottedCargoContainer()
		tray.add_resource_slot(Fish, 10)
		with self.assertRaises(CargoContainerException) as error_context:
			tray.add_resource_slot(Fish, 12)
		self.assertIn(
			"An input slot of that resource type has already been added",
			error_context.exception.message,
			)

	def test_can_hold_cargo_returns_true_if_slot_is_available(self):
		tray = SlottedCargoContainer()
		tray.add_resource_slot(Fish, 1)
		self.assertTrue(tray.can_hold_cargo(Fish))

	def test_can_hold_cargo_returns_true_if_slot_is_not_available(self):
		tray = SlottedCargoContainer()
		self.assertFalse(tray.can_hold_cargo(Fish))

	def test_load_cargo_increases_load_of_slot_if_tray_can_hold_the_resource(self):  # noqa
		tray = SlottedCargoContainer()
		tray.add_resource_slot(Fish, 1)
		remains = tray.load_cargo(Fish, 1)
		self.assertEqual(tray.current_load(Fish), 1)
		self.assertEqual(remains, 0)

	def test_load_cargo_increases_load_of_slot_if_tray_can_hold_the_resource_and_returns_excess_that_could_not_be_loaded(self):  # noqa
		tray = SlottedCargoContainer()
		tray.add_resource_slot(Fish, 3)
		remains = tray.load_cargo(Fish, 7)
		self.assertEqual(tray.current_load(Fish), 3)
		self.assertEqual(remains, 4)

	def test_load_cargo_returns_entire_load_if_slot_is_already_at_capacity(self):  # noqa
		tray = SlottedCargoContainer()
		tray.add_resource_slot(Fish, 3)
		tray.get_slot(Fish)['load'] = 3
		remains = tray.load_cargo(Fish, 7)
		self.assertEqual(tray.current_load(Fish), 3)
		self.assertEqual(remains, 7)

	def test_load_cargo_raises_exception_if_tray_cannot_hold_the_resource(self):  # noqa
		tray = SlottedCargoContainer()
		with self.assertRaises(CargoContainerException) as error_context:
			tray.load_cargo(Fish, 1)
		self.assertIn(
			"A cargo slot of that type has not been added",
			error_context.exception.message,
			)

	def test_unload_cargo_decreases_load_of_slot_if_tray_can_hold_the_resource_and_all_available_cargo_up_to_the_requested_quantity(self):  # noqa
		tray = SlottedCargoContainer()
		tray.add_resource_slot(Fish, 3)
		tray.get_slot(Fish)['load'] = 3
		load = tray.unload_cargo(Fish, 7)
		self.assertEqual(tray.current_load(Fish), 0)
		self.assertEqual(load, 3)

	def test_unload_cargo_returns_nothing_if_slot_is_empty(self):
		tray = SlottedCargoContainer()
		tray.add_resource_slot(Fish, 3)
		load = tray.unload_cargo(Fish, 7)
		self.assertEqual(tray.current_load(Fish), 0)
		self.assertEqual(load, 0)

	def test_unload_cargo_raises_exception_if_tray_cannot_hold_the_resource(self):  # noqa
		tray = SlottedCargoContainer()
		with self.assertRaises(CargoContainerException) as error_context:
			tray.unload_cargo(Fish, 1)
		self.assertIn(
			"A cargo slot of that type has not been added",
			error_context.exception.message,
			)
