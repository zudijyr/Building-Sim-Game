import unittest
from unittest.mock import MagicMock

from sim.models.actions.deliver import Deliver

class DeliverTest(unittest.TestCase):

	def test_is_possible_returns_false_if_the_unit_has_less_than_1_of_the_resource(self):
		dummy_resource = MagicMock()
		dummy_resource.transfer_rate = 1
		dummy_unit = MagicMock()
		dummy_unit.container.current_load.return_value = 0
		dummy_building = MagicMock()
		dummy_building.container.remaining_capacity.return_value = 2.0
		dummy_unit.target = dummy_building
		deliver = Deliver(dummy_resource, 1)
		self.assertFalse(deliver.is_possible(dummy_unit, 1.0))

	def test__execute_loads_resource_into_targets_cargo_container_based_on_the_transfer_rate_and_dt(self):
		dummy_resource = MagicMock()
		dummy_resource.transfer_rate = 1
		dummy_unit = MagicMock()
		dummy_unit.container.current_load.return_value = 2.0
		dummy_building = MagicMock()
		dummy_building.container.remaining_capacity.return_value = 2.0
		dummy_unit.target = dummy_building
		deliver = Deliver(dummy_resource, 2)

		self.assertEqual(deliver.quantity, 2)
		deliver._execute(dummy_unit, 2)
		dummy_unit.container.unload_cargo.assert_called_once_with(
			dummy_resource,
			2,
		)
		dummy_building.container.load_cargo.assert_called_once_with(
			dummy_resource,
			2,
		)
