from sim.models.actions import Action, ActionException

class Construct(Action):

	def __repr__(self):
		return 'Construct {} ({:.2f} seconds remaining)'.format(
			self.building.name,
			self.seconds_remaining,
			)

	def setup(self, building):
		self.building = building

	def is_possible(self, unit, dt):
		if not unit.can_construct_building(self.building):
			return False
		else:
			return True

	def is_complete(self, unit, dt):
		return self.elapsed_time >= self.building.build_time

	def finish(self, unit, dt):
		completed_building = unit.construct_building(self.building)
		unit.tile_map.place_building(completed_building, unit.pt)

	@property
	def seconds_remaining(self):
		return self.building.build_time - self.elapsed_time

