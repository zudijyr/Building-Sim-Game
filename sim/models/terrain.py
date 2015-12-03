from enum import Enum, unique

@unique
class TerrainType(Enum):
	land  = 1
	water = 2

class Terrain:
	terrain_type = TerrainType.land
	movement_factor = 1.0
	name = 'base terrain'

	def __repr__(self):
		return name

	def __hash__(self):
		return name.__hash__()

class Forest(Terrain):
	name = 'forest'
	movement_factor = 0.25

class Grass(Terrain):
	name = 'grass'
	movement_factor = 0.5

class Plains(Terrain):
	name = 'plains'
	movement_factor = 0.75

class Water(Terrain):
	terrain_type = TerrainType.water
	name = 'water'
	movement_factor = 1.0

