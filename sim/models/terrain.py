class Terrain:
	movement_factor = 1.0
	name = 'base terrain'

	def __repr__(self):
		return name

	def __hash__(self):
		return name.__hash__()

class LandTerrain(Terrain):
	name = 'land'
	is_water = False

class WaterTerrain(Terrain):
	name = 'water'
	is_water = True

class Forest(LandTerrain):
	name = 'forest'
	movement_factor = 0.25

class Grass(LandTerrain):
	name = 'grass'
	movement_factor = 0.5

class Water(WaterTerrain):
	name = 'water'
	movement_factor = 1.0

class Plains(LandTerrain):
	name = 'plains'
	movement_factor = 0.75

