#!/usr/bin/python
import terrain

class Tile:

	def __init__(self, terrain_type, x_position, y_position):
		self.terrain_type = terrain_type
		self.x_position = x_position
		self.y_position = y_position
   
	def displayTile(self):
		print 'terrain_type : ', self.terrain_type, 'x_position : ', self.x_position, 'y_position : ', self.y_position 

tile1 = Tile(terrain.Grass, 1,2)
assert(tile1.terrain_type.move_cost == 2)
