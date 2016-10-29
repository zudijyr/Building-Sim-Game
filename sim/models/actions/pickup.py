from sim.models.actions.deliver import Deliver
import math


class Pickup(Deliver):

	def is_possible(self, unit, dt):
		if unit.target is None:
			return False
		if unit.container.remaining_capacity(self.resource) <= 0:
			return False
		return True

	def _execute(self, unit, dt):
		self.transferred_quantity += min(dt * self.resource.transfer_rate, self.quantity)
		if self.transferred_quantity >= 1:
			self.transferred_quantity = math.floor(self.transferred_quantity)
			unit.container.load_cargo(self.resource, self.transferred_quantity)
			unit.target.container.unload_cargo(self.resource, self.transferred_quantity)
			self.quantity -= self.transferred_quantity
			self.transferred_quantity = 0

	def is_complete(self, unit, dt):
		return (self.quantity < 1.0) | (unit.target.container.current_load(self.resource) < 1.0)
