from sim import SimException

from sim.models.cargo_container import MixedCargoContainer

from uuid import uuid4
from textwrap import indent


class UnitException(SimException):
	pass


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
		self.carryable_resources = set()
		self.pt = None
		self.traversable_terrain_types = set()
		self.target = None

	def __repr__(self):
		return self.name

	@property
	def status(self):
		return '\n'.join([
			'unit type:        {}'.format(self.name),
			'movement speed:   {}'.format(self.movement_speed),
			'current position: {}'.format(self.pt),
			'current action:   {}'.format(self.current_action),
			'container:\n{}'.format(indent(str(self.container), '  '))
			])

	@property
	def current_action(self):
		if len(self.action_queue) == 0:
			return None
		else:
			return self.action_queue[0]

	@property
	def tile(self):
		return self.tile_map.get_tile(self.pt)

	def add_harvestable_resource(self, resource):
		self.harvestable_resources.add(resource)

	def add_carryable_resource(self, resource):
		self.carryable_resources.add(resource)

	def can_harvest_resource(self, resource):
		return resource in self.harvestable_resources

	def move(self, v):
		if self.tile_map is None:
			raise UnitException("The unit is not yet placed on the map")
		new_pt = self.pt + v
		if new_pt not in self.tile_map:
			raise UnitException("Unit may not move out of bounds")
		tile = self.tile_map.get_tile(new_pt)
		if tile.terrain.terrain_type not in self.traversable_terrain_types:
			message = "This unit cannot traverse "
			message += str(tile.terrain.terrain_type)
			raise UnitException(message)
		self.pt = new_pt

	def add_building_factory(self, building_factory):
		if building_factory.product.name in self.building_factories:
			message = "A factory for that building has already been added"
			raise UnitException(message)
		factory_key = building_factory.product.name
		self.building_factories[factory_key] = building_factory

	def receive_cargo(self, resource_type, quantity):
		return self.container.load_cargo(resource_type, quantity)

	def deliver_cargo(self, resource_type, quantity):
		return self.container.unload_cargo(resource_type, quantity)

	def can_construct_building(self, building):
		if self.tile_map is None:
			return False
		if building.name not in self.building_factories:
			return False
		factory = self.building_factories[building.name]
		if not factory.can_consume(self.container):
			return False
		if (building.name == "iron mine" and
				self.tile.terrain_improvement.name != "iron ore deposit"):
			# TODO make this more generalizable
			return False
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
