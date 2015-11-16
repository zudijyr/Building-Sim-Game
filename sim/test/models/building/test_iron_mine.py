import unittest
from sim.models.building.iron_mine import IronMine
from sim.models.resource import IronOre

class IronMineModelTest(unittest.TestCase):

	def test_iron_mine_produces_cabbage_from_wood(self):
		mine = IronMine()
		mine.produce_resources()
		mine.produce_resources()
		self.assertEqual(mine.deliver_cargo(IronOre, 10), 2)
