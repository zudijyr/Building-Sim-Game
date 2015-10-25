#!/usr/bin/python
import resource
import curses
import terrain

class Unit:
	curses.initscr()
	curses.start_color()
	cargo_cap = 0
	move = 0
	display_char = ''
	display_color = curses.COLOR_WHITE
	color_pair = curses.color_pair(0)
	#This feels clunky to have color_pair be a unit attribute.  Is there a better way?
	#But it's good enough for now, especially if I'm going to change to real graphics later

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

	def move_unit(self, window, x_move, y_move):
		window.addch(self.y_position,self.x_position,' ',self.color_pair)
		self.x_position += x_move
		self.move_remaining -= x_move
		self.y_position += y_move
		self.move_remaining -= y_move
		window.addch(self.y_position,self.x_position,self.display_char,self.color_pair)
		#TODO change this to reduce the move_remaining by the moveCost of the terrain

class Peasant(Unit):
	cargo_cap = 5
	move = 5
	display_char = 'P'
	display_color = curses.COLOR_RED
	curses.init_pair(5, display_color, curses.COLOR_GREEN)
	color_pair = curses.color_pair(5)

	def __init__(self, x_position, y_position, cargo_type):
		Unit.__init__(self, x_position, y_position, cargo_type)

class Ship(Unit):
	cargo_cap = 10
	move = 10
	display_char = 'S'
	display_color = curses.COLOR_MAGENTA
	curses.init_pair(6, display_color, curses.COLOR_BLUE)
	color_pair = curses.color_pair(6)

	def __init__(self, x_position, y_position, cargo_type):
		Unit.__init__(self, x_position, y_position, cargo_type)

unit1 = Peasant(1,1, resource.NullResource)
unit2 = Ship(5,5, resource.Fish)
assert(unit1.cargo_cap == 5)
assert(unit1.move_remaining == 5)
assert unit1.cargo_type.name == 'null resource'
assert unit2.cargo_type.name == 'fish'

#TODO figure out a way to test move_unit without starting a window here
#unit1.move_unit(3,0, terrain.Hill)
#unit2.move_unit(0,7, terrain.Hill)
#assert(unit1.x_position == 4)
#assert(unit2.y_position == 12)
