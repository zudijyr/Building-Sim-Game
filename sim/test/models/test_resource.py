import unittest
from sim.models.resource import *

class ResourceModelTest(unittest.TestCase):

	def test_resources_are_hashable_by_their_name(self):
		resource_dict = {}
		resource_dict[Cabbage] = 'test cabbage'
		self.assertEqual(resource_dict[Cabbage], 'test cabbage')
