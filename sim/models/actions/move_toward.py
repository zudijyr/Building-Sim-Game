from sim.models.actions import Action
from sim.models.unit import UnitException


class MoveToward(Action):

	def __repr__(self):
		return 'Move Toward {}'.format(self.dest_pt)

	def setup(self, dest_pt):
		self.dest_pt = dest_pt
		self.is_obstructed = False

	def is_possible(self, unit, dt):
		if unit.tile_map is None:
			return False
		elif self.dest_pt.near(unit.pt):
			return False
		else:
			return True

	def _execute(self, unit, dt):
		tile = unit.tile
		movement_factor = (tile.terrain.movement_factor *
						   tile.terrain_improvement.movement_factor)
		speed = (unit.movement_speed * movement_factor *
				 unit.tile_map.tile_sz.diag)

		dest_v = self.dest_pt - unit.pt
		possible_distance = min(speed * dt, dest_v.M)
		move_v = dest_v.u * possible_distance
		try:
			unit.move(move_v)
		except UnitException:
			self.is_obstructed = True

	def is_complete(self, unit, dt):
		return unit.pt.near(self.dest_pt) or self.is_obstructed
