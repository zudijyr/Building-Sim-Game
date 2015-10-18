#!/usr/bin/python

class Terrain:
	move_cost = 1
	name = 'base terrain'

	def display_terrain():
		print 'Name : ', name

class Plains(Terrain):
	name = 'plains'
	move_cost = 2

class Hill(Terrain):
	name = 'hill'
	move_cost = 4

terrain1 = Plains()
terrain2 = Hill()
assert(terrain1.name == 'plains')
assert(terrain1.move_cost == 2)
assert(terrain2.name == 'hill')
assert(terrain2.move_cost == 4)
