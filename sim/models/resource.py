from sim.models.terrain import Forest

class Resource:
	name = ''
	weight = 1
	harvestable_from = []
	harvest_rate = 0.0

	def __repr__(self):
		return name

	def __hash__(self):
		return name.__hash__()

class Cabbage(Resource):
	name = 'cabbage'
	weight = 1

class Wood(Resource):
	name = 'wood'
	weight = 2
	harvestable_from = [ Forest ]
	harvest_rate = 0.5

class Fish(Resource):
	name = 'fish'
	weight = 2

class Stone(Resource):
	name = 'stone'
	weight = 5

class Lumber(Resource):
	name = 'lumber'
	weight = 3

class NullResource(Resource):
	name = 'null resource'
	weight = 0
