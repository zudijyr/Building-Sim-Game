#!/usr/bin/python
import resource

class Unit:
	cargo_cap = 0
	move = 0
	display_char = ''

	def __init__(self, x_position, y_position, cargo_type):
		self.cargo_load = 0
		self.move_remaining = self.move
		self.x_position = x_position
		self.y_position = y_position
		self.cargo_type = cargo_type
   
	def display_cargo_load(self):
		print "Total cargo_load %d" % Unit.cargo_load

	def display_unit(self):
		print "Move: ", self.move, ", cargo_cap: ", self.cargo_cap
		print "x_position : ", self.x_position,  ", y_position: ", self.y_position, ", cargo_type: ", self.cargo_type

	def move_unit(self, x_move, y_move):
		self.x_position += x_move
		self.move_remaining -= x_move
		self.y_position += y_move
		self.move_remaining -= y_move
		#TODO change this to reduce the move_remaining by the moveCost of the terrain

class Peasant(Unit):
	cargo_cap = 5
	move = 5
	display_char = 'P'

	def __init__(self, x_position, y_position, cargo_type):
		Unit.__init__(self, x_position, y_position, cargo_type)

class Ship(Unit):
	cargo_cap = 10
	move = 10
	display_char = 'S'

	def __init__(self, x_position, y_position, cargo_type):
		Unit.__init__(self, x_position, y_position, cargo_type)

unit1 = Peasant(1,1, resource.NullResource)
unit2 = Ship(5,5, resource.Fish)
assert(unit1.cargo_cap == 5)
assert(unit1.move_remaining == 5)
assert unit1.cargo_type.name == 'null resource'
assert unit2.cargo_type.name == 'fish'
unit1.move_unit(3,0)
unit2.move_unit(0,7)
assert(unit1.x_position == 4)
assert(unit2.y_position == 12)
