class Resource:
	name = ''
	weight = 1

	def __repr__(self):
		return name

class Cabbage(Resource):
	name = 'cabbage'
	weight = 1

class Wood(Resource):
	name = 'wood'
	weight = 2

class Fish(Resource):
	name = 'fish'
	weight = 2

class Stone(Resource):
	name = 'stone'
	weight = 5

class NullResource(Resource):
	name = 'null resource'
	weight = 0
