#!/usr/bin/python

import Resource
import Unit

class Building:
	inputCap = 0
	inputLoad = 0
	inputType = Resource.NullResource
	outputCap = 0
	outputLoad = 0
	outputType = ''

	def __init__(self, xPosition, yPosition):
		self.xPosition = xPosition
		self.yPosition = yPosition

	def produce(self):
		self.inputLoad -= 1 #needs error check
		self.outputLoad += 1

	def unloadUnitCargoIntoBuilding(self, unit):
		#needs error check
		self.inputLoad = unit.cargoLoad
		unit.cargoLoad = 0

	def loadBuildingCargoIntoUnit(self, unit):
		#needs error check
		unit.cargoLoad = self.outputLoad
		unit.cargoType = self.outputType
		self.outputLoad = 0
   
	def displayOutputLoad(self):
		print "Total outputLoad %d" % Building.outputLoad

	def displayBuilding(self):
		print "xPosition : ", self.xPosition,  ", yPosition: ", self.yPosition, ", outputType: ", self.outputType

class cabbagePatch(Building):
	inputCap = 5
	outputCap = 5
	outputType = Resource.Cabbage

	def __init__(self, xPosition, yPosition):
		Building.__init__(self, xPosition, yPosition)

class fishingHole(Building):
	inputCap = 5
	outputCap = 5
	outputType = Resource.Fish

	def __init__(self, xPosition, yPosition):
		Building.__init__(self, xPosition, yPosition)

building1 = cabbagePatch(1,1,)
building2 = fishingHole(5,5)
assert(building1.inputCap == 5)
assert(building2.outputType == Resource.Fish)

unit1 = Unit.Peasant("peasant", 1,1, "null")
unit1.cargoLoad = 5
unit2 = Unit.Ship("ship", 5,5, "null")
unit2.cargoLoad = 5
building1.unloadUnitCargoIntoBuilding(unit1)
building2.unloadUnitCargoIntoBuilding(unit2)
assert(building1.inputLoad == 5)
assert(unit1.cargoLoad == 0)

building1.produce()
building2.produce()
assert(building1.inputLoad == 4)
assert(building2.outputLoad == 1)

building1.loadBuildingCargoIntoUnit(unit1)
building2.loadBuildingCargoIntoUnit(unit2)
assert(unit1.cargoType == Resource.Cabbage)
assert(unit2.cargoType == Resource.Fish)
