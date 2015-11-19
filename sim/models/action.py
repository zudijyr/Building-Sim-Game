from sim import SimException
from sim.models.resource import Resource

class ActionException(SimException) : pass

class Action:

	def __init__(self, *args, **kwds):
		self.elapsed_time = 0.0
		self.setup(*args, **kwds)

	def __repr__(self):
		return 'base_action'

	def setup(self, *args, **kwds):
		pass

	def is_possible(self, unit, dt):
		return True

	def execute(self, unit, dt):
		pass

	def is_complete(self, unit, dt):
		pass

	def finish(self, unit, dt):
		pass

	def next_action(self, unit, dt):
		return self

class Harvest(Action):

	def setup(self, resource, quantity=1):
		self.initial_quantity = quantity
		self.quantity = quantity
		self.resource = resource

	def __repr__(self):
		return 'Harvest {} {} ({:.2f} remaining)'.format(
			self.initial_quantity,
			self.resource.name,
			self.quantity,
			)

	def is_possible(self, unit, dt):
		if unit.tile.terrain not in self.resource.harvestable_from:
			print("{} can't harvest {} from {}".format(unit.name, self.resource.name, unit.tile.terrain.name))
			return False
		if unit.container.remaining_capacity(self.resource) <= 0:
			print("{} can't harvest {}; no remaining capacity".format(unit.name, self.resource.name))
			return False
		return True

	def execute(self, unit, dt):
		gathered_quantity = min(dt * self.resource.harvest_rate, self.quantity)
		unit.container.load_cargo(self.resource, gathered_quantity)
		self.quantity -= gathered_quantity

	def is_complete(self, unit, dt):
		return self.quantity <= 0.0

class MoveToward(Action):

	def __repr__(self):
		return 'Move Toward {}'.format(
			self.dest_pt,
			)

	def setup(self, dest_pt, is_grid_pt=False):
		self.dest_pt = dest_pt
		self.is_grid_pt = is_grid_pt

	def is_possible(self, unit, dt):
		if unit.tile_map is None:
			return False
		elif self.dest_pt == unit.tile_map.get_unit_position(unit):
		    return False
		else:
			return True

	def execute(self, unit, dt):
		if self.is_grid_pt is True:
			self.dest_pt = unit.tile_map.grid_coords_to_map_coords(self.dest_pt)
			self.dest_pt += unit.tile_map.tile_sz * 0.5
			self.is_grid_pt = False

		tile = unit.tile
		movement_factor = tile.terrain.movement_factor * tile.terrain_improvement.movement_factor
		speed = unit.movement_speed * movement_factor * unit.tile_map.tile_sz.diag

		dest_v  = self.dest_pt - unit.pt
		possible_distance = min(speed * dt, dest_v.M)
		move_v = dest_v.u * possible_distance
		unit.move(move_v)

	def is_complete(self, unit, dt):
		return unit.pt.near(self.dest_pt)

class ConstructBuilding(Action):

	def __repr__(self):
		return 'Construct {} ({:.2f} seconds remaining)'.format(
			self.building.name,
			self.seconds_remaining,
			)

	@property
	def seconds_remaining(self):
		return self.building.build_time - self.elapsed_time

	def setup(self, building):
		self.building = building

	def is_possible(self, unit, dt):
		if not unit.can_construct_building(self.building):
			print("{} can't build {}".format(unit.name, self.building.name))
			return False
		else:
			return True

	def execute(self, unit, dt):
		self.elapsed_time += dt

	def is_complete(self, unit, dt):
		return self.elapsed_time >= self.building.build_time

	def finish(self, unit, dt):
		completed_building = unit.construct_building(self.building)
		unit.tile_map.place_building(completed_building, unit.pt)


