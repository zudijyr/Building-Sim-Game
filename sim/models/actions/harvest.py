from sim.models.actions import Action
import math


class Harvest(Action):

	def setup(self, resource, quantity):
		self.initial_quantity = quantity
		self.quantity = quantity
		self.resource = resource
		self.gathered_quantity = 0

	def __repr__(self):
		return 'Harvest {} {} ({:.2f} remaining)'.format(
			self.initial_quantity,
			self.resource.name,
			self.quantity-self.gathered_quantity,
			)

	def is_possible(self, unit, dt):
		if unit.tile.terrain not in self.resource.harvestable_from:
			return False
		if unit.container.remaining_capacity(self.resource) <= 0:
			return False
		return True

	def _execute(self, unit, dt):
		self.gathered_quantity += min(dt * self.resource.harvest_rate, self.quantity)
		if self.gathered_quantity > 1:
			self.gathered_quantity = math.floor(self.gathered_quantity)
			unit.container.load_cargo(self.resource, self.gathered_quantity)
			self.quantity -= self.gathered_quantity
			self.gathered_quantity = 0

	def is_complete(self, unit, dt):
		return self.quantity < 1.0
