import unittest
from sim.models.building.cabbage_farm import CabbageFarm
from sim.models.resource import Cabbage, Wood


class CabbageFarmModelTest(unittest.TestCase):

	def test_cabbage_farm_produces_cabbage_from_wood(self):
		farm = CabbageFarm()
		farm.receive_cargo(Wood, 3)
		farm.produce_resources()
		farm.produce_resources()
		self.assertEqual(farm.deliver_cargo(Cabbage, 10), 2)
