import unittest
from unittest.mock import MagicMock

from sim.models.actions.harvest import Harvest


class HarvestTest(unittest.TestCase):

	def test_is_possible_returns_false_if_the_resource_is_not_harvestable_from_the_units_current_terrain(self):  # noqa
		dummy_resource = MagicMock()
		dummy_resource.harvestable_from = set()
		dummy_unit = MagicMock()
		dummy_unit.tile.terrain = 'dummy_terrain'
		harvest = Harvest(dummy_resource, 1)
		self.assertFalse(harvest.is_possible(dummy_unit, 1.0))

	def test_is_possible_returns_false_if_the_units_remaining_capacity_for_the_target_resource_is_zero(self):  # noqa
		dummy_resource = MagicMock()
		dummy_resource.harvestable_from = set(['dummy_terrain'])
		dummy_unit = MagicMock()
		dummy_unit.tile.terrain = 'dummy_terrain'
		dummy_unit.container.remaining_capacity.return_value = 0.0
		harvest = Harvest(dummy_resource, 1)
		self.assertFalse(harvest.is_possible(dummy_unit, 1.0))

	def test_is_possible_returns_true_if_the_units_can_harvest_the_target_resource(self):  # noqa
		dummy_resource = MagicMock()
		dummy_resource.harvestable_from = set(['dummy_terrain'])
		dummy_unit = MagicMock()
		dummy_unit.tile.terrain = 'dummy_terrain'
		dummy_unit.container.remaining_capacity.return_value = 1.0
		harvest = Harvest(dummy_resource, 1)
		self.assertTrue(harvest.is_possible(dummy_unit, 1.0))

	def test__execute_loads_resource_into_units_cargo_container_based_on_the_harvest_rate_and_dt(self):  # noqa
		dummy_resource = MagicMock()
		dummy_resource.harvest_rate = 0.5
		dummy_unit = MagicMock()
		harvest = Harvest(dummy_resource, 1)
		harvest._execute(dummy_unit, 1.0)
		dummy_unit.container.load_cargo.assert_called_once_with(
			dummy_resource,
			0.5,
			)
		self.assertEqual(harvest.quantity, 0.5)

	def test__execute_will_not_load_more_resources_than_the_requested_quantity_even_if_the_rate_by_dt_is_larger(self):  # noqa
		dummy_resource = MagicMock()
		dummy_resource.harvest_rate = 3
		dummy_unit = MagicMock()
		harvest = Harvest(dummy_resource, 2.0)
		harvest._execute(dummy_unit, 1.0)
		dummy_unit.container.load_cargo.assert_called_once_with(
			dummy_resource,
			2.0,
			)
		self.assertEqual(harvest.quantity, 0.0)

	def test_is_complete_returns_true_if_and_only_if_the_remaining_quantity_is_less_than_or_equal_to_zero(self):  # noqa
		dummy_resource = MagicMock()
		dummy_unit = MagicMock()
		harvest = Harvest(dummy_resource, 1.0)
		self.assertFalse(harvest.is_complete(dummy_unit, 1.0))
		harvest.quantity = -0.000001
		self.assertTrue(harvest.is_complete(dummy_unit, 1.0))
