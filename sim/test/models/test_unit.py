import unittest
from sim.models.unit import Unit, UnitException
from sim.models.tile_map import TileMap
from sim.models.terrain import Plains
from sim.models.terrain_improvement import Road

class DummyUnit(Unit):
    strength = 10
    movement_speed = 10

class UnitModelTest(unittest.TestCase):

    def test_move_unit_one_moves_the_unit_by_the_specified_change_in_x_and_y(self):
        tmap = TileMap(0, 0, 10, 10)
        tmap.set_terrain(Plains, 6,6)
        tmap.set_terrain(Plains, 7,7)
        unit = DummyUnit()
        tmap.place_unit(unit, 5, 5)
        unit.move_unit_one((1, 1))
        unit.move_unit_one((1, 1))
        self.assertEqual(unit.moves_remaining, 10 - Plains.move_cost * 2)

    def test_move_unit_one_does_not_move_the_unit_if_the_move_would_go_over_the_map_boundary(self):
        tmap = TileMap(0, 0, 10, 10)
        unit = DummyUnit()
        tmap.place_unit(unit, 9, 5)
        unit.move_unit_one((1, 0))
        (x, y) = tmap.get_unit_position(unit)
        self.assertEqual(x, 9)
        self.assertEqual(y, 5)

    def test_move_unit_one_raises_an_exception_if_the_absolute_value_of_the_move_in_x_or_y_is_greater_than_1(self):
        tmap = TileMap(0, 0, 10, 10)
        unit = DummyUnit()
        tmap.place_unit(unit, 0, 0)
        with self.assertRaises(UnitException) as error_context:
            unit.move_unit_one((2, 0))
        self.assertEqual("Must move 1 at a time in x and or y", error_context.exception.message)

    def test_move_unit_one_moves_faster_along_road(self):
        tmap = TileMap(0, 0, 10, 10)
        unit = DummyUnit()
        tmap.place_unit(unit, 0, 0)
        tmap.set_terrain(Plains, 1, 1)
        tmap.set_terrain_improvement(Road, 1, 1)
        unit.move_unit_one((1, 1))
        self.assertEqual(unit.moves_remaining, 10 - (Plains.move_cost)/2)

    def test_set_path_creates_path_straight_from_initial_to_final_position(self):
        tmap = TileMap(0, 0, 10, 10)
        unit = DummyUnit()
        tmap.place_unit(unit, 0, 0)
        unit.set_path(5,5)
        self.assertEqual(unit.path, [(1,1),(1,1),(1,1),(1,1),(1,1)] )

    def test_set_path_creates_path_makes_diagonal_moves_first(self):
        tmap = TileMap(0, 0, 10, 10)
        unit = DummyUnit()
        tmap.place_unit(unit, 0, 0)
        unit.set_path(3,5)
        self.assertEqual(unit.path, [(1,1),(1,1),(1,1),(0,1),(0,1)] )


