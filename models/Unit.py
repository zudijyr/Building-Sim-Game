#!/usr/bin/python
import Resource

class Unit:
	cargoCap = 0
	move = 0

	def __init__(self, name, xPosition, yPosition, cargoType):
		self.cargoLoad = 0
		self.name = name
		self.moveRemaining = self.move
		self.xPosition = xPosition
		self.yPosition = yPosition
		self.cargoType = cargoType
   
	def displayCargoLoad(self):
		print "Total cargoLoad %d" % Unit.cargoLoad

	def displayUnit(self):
		print "Name : ", self.name, ", Move: ", self.move, ", cargoCap: ", self.cargoCap
		print "xPosition : ", self.xPosition,  ", yPosition: ", self.yPosition, ", cargoType: ", self.cargoType

	def moveUnit(self, xMove, yMove):
		self.xPosition += xMove
		self.moveRemaining -= xMove
		self.yPosition += yMove
		self.moveRemaining -= yMove
		#TODO change this to reduce the moveRemaining by the moveCost of the terrain

class Peasant(Unit):
	cargoCap = 5
	move = 5

	def __init__(self, name, xPosition, yPosition, cargoType):
		Unit.__init__(self, name, xPosition, yPosition, cargoType)

class Ship(Unit):
	cargoCap = 10
	move = 10

	def __init__(self, name, xPosition, yPosition, cargoType):
		Unit.__init__(self, name, xPosition, yPosition, cargoType)

unit1 = Peasant("Peasant", 1,1, "null")
unit2 = Ship("Ship", 5,5, "fish")
assert(unit1.cargoCap == 5)
assert(unit1.moveRemaining == 5)
unit1.moveUnit(3,0)
unit2.moveUnit(0,7)
assert(unit1.xPosition == 4)
assert(unit2.yPosition == 12)
