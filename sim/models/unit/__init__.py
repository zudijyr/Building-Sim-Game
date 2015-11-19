from sim import SimException
from sim.models.tile_map import TileMap
from sim.models.tile_grid import TileGrid
from sim.models.cargo_container import MixedCargoContainer

import sys
from uuid import uuid4
from textwrap import indent

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
		self.harvestable_resources = set()

	def __repr__(self):
		return self.name

	@property
	def status(self):
		return '\n'.join([
			'unit type:        {}'.format(self.name),
			'unit id:          {}'.format(self.unit_id),
			'movement speed:   {}'.format(self.movement_speed),
			'current position: {}'.format(self.pt),
			'current action:   {}'.format(self.current_action),
			'container:\n{}'.format(indent(str(self.container), '  '))
			])

	def set_tile_map(self, tile_map):
		self.tile_map = tile_map

	@property
	def current_action(self):
		if len(self.action_queue) == 0:
			return None
		else:
			return self.action_queue[0]

	@property
	def tile(self):
		return self.tile_map.get_tile_under_unit(self)

	@property
	def pt(self):
		return self.tile_map.get_unit_position(self)

	def add_harvestable_resource(self, resource):
		self.harvestable_resources.add(resource)

	def can_harvest_resource(self, resource):
		return resource in self.harvestable_resources

	def move(self, v):
		self.tile_map.move_unit(self, v)

	def add_building_factory(self, building_factory):
		if building_factory.product.name in self.building_factories:
			raise UnitException("A factory for that building has already been added")
		self.building_factories[building_factory.product.name] = building_factory

	def receive_cargo(self, resource_type, quantity):
		return self.container.load_cargo(resource_type, quantity)

	def deliver_cargo(self, resource_type, quantity):
		return self.container.unload_cargo(resource_type, quantity)

	def can_construct_building(self, building):
		if self.tile_map is None:
			return False
		if not building.name in self.building_factories:
			return False
		if not self.building_factories[building.name].can_consume(self.container):
			return False
		if building.name == "iron mine" and self.tile.terrain_improvement.name != "iron ore deposit":
			return False #TODO make this more generalizable
		return True

	def construct_building(self, building):
		if building.name not in self.building_factories:
			raise UnitException("This unit cannot build that building")
		return self.building_factories[building.name].digest(self.container)

	def act(self, dt):
		if len(self.action_queue) == 0:
			return
		action = self.action_queue.pop(0)
		if not action.is_possible(self, dt):
			return
		action.execute(self, dt)
		if action.is_complete(self, dt):
			action.finish(self, dt)
		else:
			self.add_immediate_action(action.next_action(self, dt))

	def add_action(self, action):
		self.action_queue.append(action)

	def add_immediate_action(self, action):
		self.action_queue.insert(0, action)

	def clear_actions(self):
		self.action_queue = []

