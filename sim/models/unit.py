from sim.models.resource import *
from sim.models.terrain import *
from sim.models.cargo_container import MixedCargoContainer
from sim.models.tile_map import TileMap

from textwrap import indent

class UnitException(Exception):
	def __init__(self, message):
		self.message = message
	def __str__(self):
		return self.message

class Unit:
	movement_speed = 0
	display_char = ''
	strength = 0

	def __init__(self, x_position, y_position, tile_map):
		self.container = MixedCargoContainer()
		self.container.set_weight_capacity(self.strength)
		self.moves_remaining = self.movement_speed
		self.x_position = x_position
		self.y_position = y_position
		self.tile_map = tile_map
		self.path = []

	def __repr__(self):
		return '\n'.join([
			'x_position:      {}'.format(self.x_position),
			'y_position:      {}'.format(self.y_position),
			'movement_speed:  {}'.format(self.movement_speed),
			'moves_remaining: {}'.format(self.moves_remaining),
			'container:\n{}'.format(indent(str(self.container), '  '))
			])

	def receive_cargo(self, resource_type, quantity):
		return self.container.load_cargo(resource_type, quantity)

	def deliver_cargo(self, resource_type, quantity):
		return self.container.unload_cargo(resource_type, quantity)

	#def find_shortest_path(tile_map, start, end, path=[]):
	#	path = path + [start]
	#	if start == end:
	#		return path
	#	if not graph.has_key(start):
	#		return None
	#	shortest = None
	#	for node in graph[start]:
	#		if node not in path:
	#			newpath = find_shortest_path(graph, node, end, path)
	#			if newpath:
	#				if not shortest or len(newpath) < len(shortest):
	#					shortest = newpath
	#	return shortest

	def set_path(self, final_x, final_y, tile_map):
		#eventually this will calculate the lowest-cost path by something like Dijkstra's algorithm (above)
		#but for now it just goes in a straight line, starting with diagonal movement
		self.path = []
		current_x = self.x_position
		current_y = self.y_position

		while current_x < final_x and current_y < final_y:
			self.path.append((1,1))
			current_x += 1
			current_y += 1
		while current_x > final_x and current_y < final_y:
			self.path.append((-1,1))
			current_x -= 1
			current_y += 1
		while current_x < final_x and current_y > final_y:
			self.path.append((1,-1))
			current_x += 1
			current_y -= 1
		while current_x > final_x and current_y > final_y:
			self.path.append((-1,-1))
			current_x -= 1
			current_y -= 1
		while current_x < final_x:
			self.path.append((1,0))
			current_x += 1
		while current_y < final_y:
			self.path.append((0,1))
			current_y += 1
		while current_x > final_x:
			self.path.append((-1,0))
			current_x -= 1
		while current_y > final_y:
			self.path.append((0,-1))
			current_y -= 1

		assert (current_x == final_x)
		assert (current_y == final_y)

	def move_unit_one(self, move):
		x_move = move[0]
		y_move = move[1]
		if abs(x_move) > 1 or abs(y_move) > 1:
			raise UnitException("Must move 1 at a time in x and or y")

		new_x = self.x_position + x_move
		new_y = self.y_position + y_move
		if not self.tile_map.in_bounds(new_x, new_y):
			return

		raw_move_cost = self.tile_map.get_terrain(new_x, new_y).move_cost
		move_cost = raw_move_cost/(self.tile_map.get_terrain_improvement(new_x, new_y).movement_reduction)
		if self.moves_remaining - move_cost >= 0:
			self.x_position = new_x
			self.y_position = new_y
			self.moves_remaining -= move_cost


class Peasant(Unit):
	strength = 25
	movement_speed = 25
	display_char = 'P'

	def chop_wood(self):
		current_terrain = self.tile_map.get_terrain(self.x_position, self.y_position)
		if current_terrain != Forest:
			return
		if self.container.remaining_capacity(Wood) <= 0:
			return
		self.moves_remaining -= 1
		self.container.load_cargo(Wood, 1)

class Ship(Unit):
	strength = 100
	movement_speed = 30
	display_char = 'S'

