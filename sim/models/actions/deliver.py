from sim.models.actions import Action
import math


class Deliver(Action):

	def setup(self, resource, quantity):
		self.initial_quantity = quantity
		self.quantity = quantity
		self.resource = resource
		self.transferred_quantity = 0

	def __repr__(self):
		return 'Transfer {} {} ({:.2f} remaining)'.format(
			self.initial_quantity,
			self.resource.name,
			self.quantity,
			)

	def is_possible(self, unit, dt):
		if unit.target is None:
			return False
		if unit.target.container.remaining_capacity(self.resource) <= 0:
			return False
		if self.quantity < 1.0:
			return False
		return True

	def _execute(self, unit, dt):
		self.transferred_quantity += min(dt * self.resource.transfer_rate, self.quantity)
		if self.transferred_quantity >= 1:
			self.transferred_quantity = math.floor(self.transferred_quantity)
			unit.target.container.load_cargo(self.resource, self.transferred_quantity)
			unit.container.unload_cargo(self.resource, self.transferred_quantity)
			self.quantity -= self.transferred_quantity
			self.transferred_quantity = 0

	def is_complete(self, unit, dt):
		return self.quantity < 1.0
