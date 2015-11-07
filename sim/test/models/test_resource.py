import unittest
from sim.models.resource import *

class ResourceModelTest(unittest.TestCase):

    def test_null_resource_weighs_nothing(self):
        resource = NullResource()
        self.assertEqual(resource.weight, 0)
