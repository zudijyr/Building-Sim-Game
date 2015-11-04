import unittest
from sim.models.building.fishing_hole import FishingHole
from sim.models.resource import Fish

class FishingHoleModelTest(unittest.TestCase):

    def test_fishing_hole_produces_fish(self):
        hole = FishingHole()
        hole.produce_resources()
        hole.produce_resources()
        self.assertEqual(hole.deliver_cargo(Fish, 10), 6)

