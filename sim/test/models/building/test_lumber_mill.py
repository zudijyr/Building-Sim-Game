import unittest
from sim.models.resource import Lumber, Wood
from sim.models.building.lumber_mill import LumberMill

class LumberMillModelTest(unittest.TestCase):

	def test_lumber_mill_produces_lumbe_from_wood(self):
		mill = LumberMill()
		mill.receive_cargo(Wood, 3)
		mill.produce_resources()
		mill.produce_resources()
		self.assertEqual(mill.deliver_cargo(Lumber, 10), 2)
