import unittest
from sim.models.tile_map import TileMap
from sim.models.unit.peasant import Peasant
from sim.models.terrain import Forest, Plains
from sim.models.resource import Wood
from sim.models.building.cabbage_farm import CabbageFarm

class PeasantModelTest(unittest.TestCase):

    def test_chop_wood_adds_wood_to_the_peasants_cargo_and_takes_one_move(self):
        tmap = TileMap(0, 0, 10, 10)
        tmap.set_terrain(Forest, 5, 5)
        unit = Peasant()
        tmap.place_unit(unit, 5, 5)
        unit.chop_wood()
        unit.chop_wood()
        self.assertEqual(unit.deliver_cargo(Wood, 5), 2)
        self.assertEqual(unit.moves_remaining, 23)

    def test_chop_wood_does_nothing_if_the_current_terrain_is_not_forest(self):
        tmap = TileMap(0, 0, 10, 10)
        tmap.set_terrain(Plains, 5, 5)
        unit = Peasant()
        tmap.place_unit(unit, 5, 5)
        unit.chop_wood()
        self.assertEqual(unit.deliver_cargo(Wood, 5), 0)
        self.assertEqual(unit.moves_remaining, 25)

    def test_chop_wood_does_nothing_if_the_peasant_has_no_more_capacity_to_carry_wood(self):
        tmap = TileMap(0, 0, 10, 10)
        tmap.set_terrain(Forest, 5, 5)
        unit = Peasant()
        tmap.place_unit(unit, 5, 5)
        unit.container.weight_capacity = Wood.weight - 1
        unit.chop_wood()
        self.assertEqual(unit.deliver_cargo(Wood, 5), 0)
        self.assertEqual(unit.moves_remaining, 25)

    # TODO:test cabbage_farm_creation

