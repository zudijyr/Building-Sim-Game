#!/usr/bin/python

class Terrain:
	moveCost = 1
	name = 'base terrain'

	def displayTerrain():
		print 'Name : ', name

class Plains(Terrain):
	name = 'plains'
	moveCost = 2

class Hill(Terrain):
	name = 'hill'
	moveCost = 4

terrain1 = Plains()
terrain2 = Hill()
assert(terrain1.name == 'plains')
assert(terrain1.moveCost == 2)
assert(terrain2.name == 'hill')
assert(terrain2.moveCost == 4)
