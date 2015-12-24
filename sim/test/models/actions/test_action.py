import unittest
from unittest.mock import patch

from sim.models.actions import Action


class ActionTest(unittest.TestCase):

	@patch.object(Action, 'setup')
	def test_init_calls_setup_with_supplied_args_and_kwds(self, mock_setup):
		Action('arg1', 'arg2')
		mock_setup.assert_called_once_with('arg1', 'arg2')

	@patch.object(Action, '_execute')
	def test_execute_calls__execute_and_adds_dt_to_elapsed_time(self, mock__execute):  # noqa
		action = Action()
		action.execute('dummy_unit', 1.5)
		mock__execute.assert_called_once_with('dummy_unit', 1.5)
		self.assertEqual(action.elapsed_time, 1.5)
