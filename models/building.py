#!/usr/bin/python

import resource
import unit

class Building:
	input_cap = 0
	input_load = 0
	input_type = resource.NullResource
	output_cap = 0
	output_load = 0
	output_type = ''
	display_char = ''

	def __init__(self, x_position, y_position):
		self.x_position = x_position
		self.y_position = y_position

	def produce(self):
		self.input_load -= 1 #needs error check
		self.output_load += 1

	def unload_unit_cargo_into_building(self, unit):
		#needs error check
		self.input_load = unit.cargo_load
		unit.cargo_load = 0

	def load_building_cargo_into_unit(self, unit):
		#needs error check
		unit.cargo_load = self.output_load
		unit.cargo_type = self.output_type
		self.output_load = 0
   
	def display_output_load(self):
		print "Total output_load %d" % Building.output_load

	def display_building(self):
		print "x_position : ", self.x_position,  ", y_position: ", self.y_position, ", output_type: ", self.output_type

class CabbagePatch(Building):
	input_cap = 5
	output_cap = 5
	display_char = 'C'
	output_type = resource.Cabbage

	def __init__(self, x_position, y_position):
		Building.__init__(self, x_position, y_position)

class FishingHole(Building):
	input_cap = 5
	output_cap = 5
	display_char = 'F'
	output_type = resource.Fish

	def __init__(self, x_position, y_position):
		Building.__init__(self, x_position, y_position)

building1 = CabbagePatch(1,1)
building2 = FishingHole(5,5)
assert(building1.input_cap == 5)
assert(building2.output_type == resource.Fish)

unit1 = unit.Peasant(1,1, resource.Cabbage)
unit1.cargo_load = 5
unit2 = unit.Ship(5,5, resource.Fish)
unit2.cargo_load = 5
building1.unload_unit_cargo_into_building(unit1)
building2.unload_unit_cargo_into_building(unit2)
assert(building1.input_load == 5)
assert(unit1.cargo_load == 0)

building1.produce()
building2.produce()
assert(building1.input_load == 4)
assert(building2.output_load == 1)

building1.load_building_cargo_into_unit(unit1)
building2.load_building_cargo_into_unit(unit2)
assert(unit1.cargo_type == resource.Cabbage)
assert(unit2.cargo_type == resource.Fish)
assert(unit1.cargo_load == 1)
