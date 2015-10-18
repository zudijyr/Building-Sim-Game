#!/usr/bin/python

class Resource:

	def __init__(self):
		self.name = ''
   
	def display_resource(self):
		print 'Name : ', self.name

class Cabbage(Resource):

	def __init__(self):
		Resource.__init__(self)
		self.name = 'cabbage'

class Fish(Resource):

	def __init__(self):
		Resource.__init__(self)
		self.name = 'fish'

class NullResource(Resource):

	def __init__(self):
		Resource.__init__(self)
		self.name = 'null resource'


resource1 = Cabbage()
resource2 = Fish()
assert(resource1.name == 'cabbage')
assert(resource2.name == 'fish')
