#!/usr/bin/python

class Resource:
	name = ''

	def display_resource(self):
		print 'Name : ', self.name

class Cabbage(Resource):
	name = 'cabbage'

	def __init__(self):
		Resource.__init__(self)

class Fish(Resource):
	name = 'fish'

	def __init__(self):
		Resource.__init__(self)

class NullResource(Resource):
	name = 'null resource'

	def __init__(self):
		Resource.__init__(self)

assert(Cabbage.name == 'cabbage')
assert(Fish.name == 'fish')
