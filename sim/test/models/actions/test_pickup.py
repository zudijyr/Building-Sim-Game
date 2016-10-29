import unittest
from unittest.mock import MagicMock

from sim.models.actions.pickup import Pickup

class PickupTest(unittest.TestCase):

	def test_is_possible_returns_false_if_the_unit_has_no_remaining_capacity(self):
		dummy_resource = MagicMock()
		dummy_resource.transfer_rate = 1
		dummy_unit = MagicMock()
		dummy_unit.container.remaining_capacity.return_value = 0
		dummy_building = MagicMock()
		dummy_building.container.current_load.return_value = 2.0
		dummy_unit.target = dummy_building
		pickup = Pickup(dummy_resource, 1)
		self.assertFalse(pickup.is_possible(dummy_unit, 1.0))

	def test__execute_loads_resource_into_units_cargo_container_based_on_the_transfer_rate_and_dt(self):
		dummy_resource = MagicMock()
		dummy_resource.transfer_rate = 1
		dummy_unit = MagicMock()
		dummy_unit.container.current_load.return_value = 2.0
		dummy_building = MagicMock()
		dummy_building.container.remaining_capacity.return_value = 2.0
		dummy_unit.target = dummy_building
		pickup = Pickup(dummy_resource, 2)

		self.assertEqual(pickup.quantity, 2)
		pickup._execute(dummy_unit, 2)
		dummy_unit.container.load_cargo.assert_called_once_with(
			dummy_resource,
			2,
		)
		dummy_building.container.unload_cargo.assert_called_once_with(
			dummy_resource,
			2,
		)
