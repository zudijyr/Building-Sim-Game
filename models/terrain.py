#!/usr/bin/python

import curses

class Terrain:
	curses.initscr()
	curses.start_color()
	move_cost = 1
	name = 'base terrain'
	color = curses.COLOR_WHITE
	color_pair = curses.color_pair(0)

	def display_terrain():
		print 'Name : ', name

class Hill(Terrain):
	name = 'hill'
	move_cost = 4
	color = curses.COLOR_GREEN
	char_color = curses.COLOR_RED
	curses.init_pair(5, char_color, color)
	color_pair = curses.color_pair(5)

class Water(Terrain):
	name = 'water'
	move_cost = 1
	color = curses.COLOR_BLUE
	char_color = curses.COLOR_MAGENTA
	curses.init_pair(6, char_color, color)
	color_pair = curses.color_pair(6)

class Plains(Terrain):
	name = 'plains'
	move_cost = 2
	color = curses.COLOR_CYAN
	char_color = curses.COLOR_RED
	curses.init_pair(7, char_color, color)
	color_pair = curses.color_pair(7)

terrain1 = Plains()
terrain2 = Hill()
assert(terrain1.name == 'plains')
assert(terrain1.move_cost == 2)
assert(terrain2.name == 'hill')
assert(terrain2.move_cost == 4)
