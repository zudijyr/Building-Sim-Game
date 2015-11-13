from sim import SimException
from sim.models.tile_map import TileMap
from sim.models.cargo_container import MixedCargoContainer

import sys
from uuid import uuid4
from textwrap import indent

EPS = sys.float_info.epsilon

class UnitException(SimException): pass

class Unit:
	# grid units per second
	movement_speed = 0
	name = ''
	strength = 0

	def __init__(self):
		self.container = MixedCargoContainer()
		self.container.set_weight_capacity(self.strength)
		self.tile_map = None
		self.building_factories = {}
		self.unit_id = uuid4()
		self.action_queue = []

	def __repr__(self):
		return '\n'.join([
			'unit_id:         {}'.format(self.unit_id),
			'movement_speed:  {}'.format(self.movement_speed),
			'container:\n{}'.format(indent(str(self.container), '  '))
			# display actions somehow?
			])

	def set_tile_map(self, tile_map):
		if not isinstance(tile_map, TileMap):
			raise UnitException("tile_map must be an instance of TileMap")
		self.tile_map = tile_map

	def add_building_factory(self, building_factory):
		if building_factory.product.name in self.building_factories:
			raise UnitException("A factory for that building has already been added")
		self.building_factories[building_factory.product.name] = building_factory

	def receive_cargo(self, resource_type, quantity):
		return self.container.load_cargo(resource_type, quantity)

	def deliver_cargo(self, resource_type, quantity):
		return self.container.unload_cargo(resource_type, quantity)

	def can_construct_building(self, building):
		if not building.name in self.building_factories:
			return False
		if not self.building_factories[building.name].can_consume(self.container):
			return False
		return True

	def construct_building(self, building):
		if building.name not in self.building_factories:
			raise UnitException("This unit cannot build that building")
		return self.building_factories[building.name].digest(self.container)


	def act(self, dt):
		if len(self.action_queue) == 0:
			return
		self.action_queue.pop(0)(dt)

	def add_action(self, method, *args, **kwds):
		self.action_queue.append(lambda dt: method(dt, *args, **kwds))

	def add_immediate_action(self, method, *args, **kwds):
		self.action_queue.insert(0, lambda dt: method(dt, *args, **kwds))

	def clear_actions(self):
		self.action_queue = []

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

	def add_path_on_grid(self, final_pt):
		map_pt = self.tile_map.grid_coords_to_map_coords(final_pt)
		map_pt = map_pt + self.tile_map.tile_sz * 0.5
		self.add_path(map_pt)

	def add_path(self, final_pt):
		if self.tile_map is None:
			raise UnitException("This unit has not been placed on the tile map yet!")
		#eventually this will calculate the lowest-cost path by something like Dijkstra's algorithm (above)
		#but for now it just goes in a straight line, starting with diagonal movement
		self.add_action(self.move_toward, final_pt)

	def move_toward(self, dt, dest_pt):
		tile = self.tile_map.get_tile_under_unit(self)
		movement_factor = tile.terrain.movement_factor * tile.terrain_improvement.movement_factor
		speed = self.movement_speed * movement_factor * self.tile_map.tile_sz.diag

		unit_pt = self.tile_map.get_unit_position(self)
		dest_v  = dest_pt - unit_pt
		possible_distance = min(speed * dt, dest_v.M)
		move_v = dest_v.u * possible_distance
		self.tile_map.move_unit(self, move_v)
		new_pt = self.tile_map.get_unit_position(self)
		if not new_pt.near(dest_pt):
			self.add_immediate_action(self.move_toward, dest_pt)

