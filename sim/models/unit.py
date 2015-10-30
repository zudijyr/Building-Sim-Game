from sim.models import resource
from sim.models import terrain

class UnitException(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message

class Unit:
    cargo_cap = 0
    movement_speed = 0
    display_char = ''

    def __init__(self, x_position, y_position, cargo_type, terrain_map):
        self.cargo = []
        self.moves_remaining = self.movement_speed
        self.x_position = x_position
        self.y_position = y_position
        self.terrain_map = terrain_map

    def __repr__(self):
        return '\n'.join([
            'x_position:      {}'.format(self.x_position),
            'y_position:      {}'.format(self.y_position),
            'cargo:           {}'.format(join(', ', self.cargo)),
            'cargo_cap:       {}'.format(self.cargo_cap),
            'movement_speed:  {}'.format(self.movement_speed),
            'moves_remaining: {}'.format(self.moves_remaining),
            ])

    def move_unit(self, x_move, y_move):
        if abs(x_move) > 1 or abs(y_move) > 1:
            raise UnitException("Currently only support movement by 1 in x or y")
            # This is here because if the movement in x or y is greater than 1,
            # we will be skipping over the movement cost of the cells between the current
            # location and the final position
            # Will have to figure out how we want to do this
        move_cost = self.terrain_map.get_terrain(
            self.x_position + x_move,
            self.y_position - y_move,
            ).move_cost
        if self.moves_remaining - move_cost >= 0:
            self.x_position += x_move
            self.y_position -= y_move
            self.moves_remaining -= move_cost

class Peasant(Unit):
    cargo_cap = 5
    movement_speed = 25
    display_char = 'P'

    def chop_wood(self):
        current_terrain = self.terrain_map.get_terrain(self.x_position, self.y_position)
        if current_terrain == terrain.Forest and len(self.cargo) < self.cargo_cap:
            self.moves_remaining -= 1
            self.cargo.append(resource.Wood)

class Ship(Unit):
    cargo_cap = 10
    movement_speed = 30
    display_char = 'S'

