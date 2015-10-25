#!/usr/bin/python

import curses

class Terrain:
	curses.initscr()
	curses.start_color()
	move_cost = 1
	name = 'base terrain'
	color = curses.COLOR_WHITE
	char_color = curses.COLOR_RED
	curses.init_pair(1, char_color, color)
	color_pair = curses.color_pair(1)

	def display_terrain():
		print 'Name : ', name

class Forest(Terrain):
	name = 'forest'
	move_cost = 4
	color = curses.COLOR_MAGENTA
	char_color = curses.COLOR_BLACK
	curses.init_pair(2, char_color, color)
	color_pair = curses.color_pair(2)

class Grass(Terrain):
	name = 'grass'
	move_cost = 2
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
	color = curses.COLOR_RED
	char_color = curses.COLOR_BLACK
	curses.init_pair(7, char_color, color)
	color_pair = curses.color_pair(7)

terrain1 = Plains()
terrain2 = Grass()
assert(terrain1.name == 'plains')
assert(terrain1.move_cost == 2)
assert(terrain2.name == 'grass')
assert(terrain2.move_cost == 2)
