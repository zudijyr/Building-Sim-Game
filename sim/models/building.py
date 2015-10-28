from sim.models import resource
from sim.models import unit

class BuildingException(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message

class Building:
    input_cap = 5
    input_load = 0
    input_type = resource.NullResource
    output_cap = 5
    output_load = 0
    output_type = ''
    display_char = ''
    building_cost_type = ''
    building_cost = ''

    def __init__(self, x_position=0, y_position=0):
        self.x_position = x_position
        self.y_position = y_position

    def can_accept_input(self):
        return self.input_load < self.input_cap

    def accept_input(self):
        if not self.can_accept_input():
            raise BuildingException("Building is already at input capacity")
        self.input_load += 1

    def can_deliver_output(self):
        return self.output_load > 0

    def deliver_output(self):
        if not self.can_deliver_output():
            raise BuildingException("Building has no output to deliver")
        self.output_load -= 1

    def produce(self):
        if self.input_load <= 0:
            return
        if self.output_load >= self.output_cap:
            return
        self.input_load -= 1
        self.output_load += 1

    def __repr__(self):
        return '\n'.join([
            'x_position:  {}'.format(self.x_position),
            'y_position:  {}'.format(self.y_position),
            'output_type: {}'.format(self.output_type),
            'input_cap:   {}'.format(self.input_cap),
            'output_cap:  {}'.format(self.output_cap),
            'input_load:  {}'.format(self.input_load),
            'output_load: {}'.format(self.output_load),
            ])


class CabbageFarm(Building):
    input_cap = 5
    output_cap = 5
    display_char = 'C'
    output_type = resource.Cabbage
    building_cost_type = resource.Wood
    building_cost = 1

class Dock(Building):
    input_cap = 5
    output_cap = 5
    display_char = 'D'
    output_type = resource.Fish

class FishingHole(Building):
    input_cap = 5
    output_cap = 5
    display_char = 'F'
    output_type = resource.Fish

#
#building1.produce()
#building2.produce()
#assert(building1.input_load == 4)
#assert(building2.output_load == 1)
#
#building1.load_building_cargo_into_unit(unit1)
#building2.load_building_cargo_into_unit(unit2)
#assert(unit1.cargo_type == resource.Cabbage)
#assert(unit2.cargo_type == resource.Fish)
#assert(unit1.cargo_load == 1)

#building1.construct_building(unit1)
