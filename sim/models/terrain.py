class Terrain:
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

class Water(Terrain):
	name = 'water'
	movement_factor = 1.0

class Plains(Terrain):
	name = 'plains'
	movement_factor = 0.75

