from sim.models.resource import *
from sim.models.terrain import *
from sim.models.cargo_container import MixedCargoContainer

from textwrap import indent

class UnitException(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message

class Unit:
    movement_speed = 0
    display_char = ''
    strength = 0

    def __init__(self, x_position, y_position, terrain_map):
        self.container = MixedCargoContainer()
        self.container.set_weight_capacity(self.strength)
        self.moves_remaining = self.movement_speed
        self.x_position = x_position
        self.y_position = y_position
        self.terrain_map = terrain_map

    def __repr__(self):
        return '\n'.join([
            'x_position:      {}'.format(self.x_position),
            'y_position:      {}'.format(self.y_position),
            'movement_speed:  {}'.format(self.movement_speed),
            'moves_remaining: {}'.format(self.moves_remaining),
            'container:\n{}'.format(indent(str(self.container), '  '))
            ])

    def receive_cargo(self, resource_type, quantity):
        return self.container.load_cargo(resource_type, quantity)

    def deliver_cargo(self, resource_type, quantity):
        return self.container.unload_cargo(resource_type, quantity)

    def move_unit(self, x_move, y_move):
        if abs(x_move) > 1 or abs(y_move) > 1:
            raise UnitException("Currently only support movement by 1 in x or y")
            # This is here because if the movement in x or y is greater than 1,
            # we will be skipping over the movement cost of the cells between the current
            # location and the final position
            # Will have to figure out how we want to do this
        new_x = self.x_position + x_move
        new_y = self.y_position - y_move
        if not self.terrain_map.in_bounds(new_x, new_y):
            return
        move_cost = self.terrain_map.get_terrain(new_x, new_y).move_cost
        if self.moves_remaining - move_cost >= 0:
            self.x_position = new_x
            self.y_position = new_y
            self.moves_remaining -= move_cost

class Peasant(Unit):
    strength = 25
    movement_speed = 25
    display_char = 'P'

    def chop_wood(self):
        current_terrain = self.terrain_map.get_terrain(self.x_position, self.y_position)
        if current_terrain != Forest:
            return
        if self.container.remaining_capacity(Wood) <= 0:
            return
        self.moves_remaining -= 1
        self.container.load_cargo(Wood, 1)

class Ship(Unit):
    strength = 100
    movement_speed = 30
    display_char = 'S'

