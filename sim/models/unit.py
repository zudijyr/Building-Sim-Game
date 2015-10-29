from sim.models import resource
from sim.models import terrain

class Unit:
    cargo_cap = 0
    move = 0
    display_char = ''

    def __init__(self, x_position, y_position, cargo_type, terrain_map):
        self.cargo_load = 0
        self.move_remaining = self.move
        self.x_position = x_position
        self.y_position = y_position
        self.cargo_type = cargo_type
        self.terrain_map = terrain_map

    def display_cargo_load(self):
        print("Total cargo_load %d" % Unit.cargo_load)

    def display_unit(self):
        print("Move: ", self.move, ", cargo_cap: ", self.cargo_cap)
        print("x_position : ", self.x_position,  ", y_position: ", self.y_position, ", cargo_type: ", self.cargo_type)

    def move_unit(self, x_move, y_move):
        move_cost = self.terrain_map.get_terrain(
            self.x_position + x_move,
            self.y_position - y_move,
            ).move_cost
        if self.move_remaining - move_cost >= 0:
            self.x_position += x_move
            self.y_position -= y_move
            self.move_remaining -= move_cost

class Peasant(Unit):
    cargo_cap = 5
    move = 25
    display_char = 'P'

    def chop_wood(self):
        current_terrain = self.terrain_map.get_terrain(self.x_position, self.y_position)
        if current_terrain == terrain.Forest:
            self.move_remaining -= 1
            self.cargo_load += 1
            self.cargo_type = resource.Wood

class Ship(Unit):
    cargo_cap = 10
    move = 30
    display_char = 'S'

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
