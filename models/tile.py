#!/usr/bin/python
import Terrain

class Tile:

	def __init__(self, terrainType, xPosition, yPosition):
		self.terrainType = terrainType
		self.xPosition = xPosition
		self.yPosition = yPosition
   
	def displayTile(self):
		print 'terrainType : ', self.terrainType, 'xPosition : ', self.xPosition, 'yPosition : ', self.yPosition 

tile1 = Tile(Terrain.Hill, 1,2)
assert(tile1.terrainType.moveCost == 4)
