import unittest
from sim.models.building.dock import Dock
from sim.models.resource import Fish


class DockModelTest(unittest.TestCase):

	def test_dock_produces_fish(self):
		dock = Dock()
		dock.produce_resources()
		dock.produce_resources()
		self.assertEqual(dock.deliver_cargo(Fish, 10), 2)
