import unittest
from sim.models.unit import *
from sim.models import resource

class UnitModelTest(unittest.TestCase):
    pass

#unit1 = Peasant(1,1, resource.NullResource)
#unit2 = Ship(5,5, resource.Fish)
#assert(unit1.cargo_cap == 5)
#assert(unit1.move_remaining == 25)
#assert unit1.cargo_type.name == 'null resource'
#assert unit2.cargo_type.name == 'fish'

#TODO figure out a way to test move_unit without starting a window here
#unit1.move_unit(3,0, terrain.Hill)
#unit2.move_unit(0,7, terrain.Hill)
#assert(unit1.x_position == 4)
#assert(unit2.y_position == 12)
