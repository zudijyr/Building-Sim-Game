from sim import SimException
from sim.models.resource import Resource

class ActionException(SimException) : pass

class Action:

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

	def __init__(self, resource, quantity=1):
		self.initial_quantity = quantity
		self.quantity = quantity
		self.resource = resource

	def is_possible(self, unit, dt):
		if unit.tile.terrain not in self.resource.harvestable_from:
			return False
		if unit.container.remaining_capacity(self.resource) <= 0:
			return False
		return True

	def execute(self, unit, dt):
		print("{} harvesting {}".format(unit.name, self.resource.name))
		gathered_quantity = min(dt * self.resource.harvest_rate, self.quantity)
		unit.container.load_cargo(self.resource, gathered_quantity)
		self.quantity -= gathered_quantity
		print("{} has {} of {} {}".format(unit.name, unit.container.current_load(self.resource), self.initial_quantity,self.resource.name))

	def is_complete(self, unit, dt):
		return self.quantity <= 0.0

class MoveToward(Action):

	def __init__(self, dest_pt, is_grid_pt=False):
		self.dest_pt = dest_pt
		self.is_grid_pt = is_grid_pt

	def is_possible(self, unit, dt):
		return unit.tile_map is not None

	def execute(self, unit, dt):
		print("{} moving toward {}".format(unit.name, self.dest_pt))
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

	def __init__(self, building):
		self.building = building
		self.elapsed_time = 0.0

	def is_possible(self, unit, dt):
		tile = unit.tile
		return unit.can_construct_building(self.building, tile)

	def execute(self, unit, dt):
		print("{} building {}".format(unit.name, self.building.name))
		self.elapsed_time += dt
		print("{} has {} seconds remaining".format(unit.name, self.building.build_time - self.elapsed_time))

	def is_complete(self, unit, dt):
		return self.elapsed_time >= self.building.build_time

	def finish(self, unit, dt):
		completed_building = unit.construct_building(self.building)
		unit.tile_map.place_building(completed_building, unit.pt)


