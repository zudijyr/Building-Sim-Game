from sim.models.actions import Action
import math


class Produce(Action):

	def setup(self, building, resource, quantity):
		self.building = building
		self.initial_quantity = quantity
		self.quantity = quantity
		self.resource = resource
		self.produced_quantity = 0
		resource_plant = self.building.resource_plants[0] #TODO allow selecting a particular resource plant
		for value in resource_plant.resource_requirements.values():
			self.required_resource = value['type'] #TODO change this to handle using multiple resources
			self.amount_used = value['load']
		self.required_quantity = self.building.container.current_load(self.required_resource)

	def __repr__(self):
		return 'Produce {} {} ({:.2f} remaining)'.format(
			self.initial_quantity,
			self.resource.name,
			self.quantity,
			)

	def is_possible(self, building, dt):
		if self.building.container.remaining_capacity(self.resource) <= 0:
			return False
		if self.quantity < 1.0:
			return False
		return True

	def _execute(self, building, dt):
		self.produced_quantity += min(dt * self.resource.production_rate, self.quantity)
		if self.produced_quantity >= 1:
			self.produced_quantity = math.floor(self.produced_quantity)
			self.building.produce_resources() #add options to specific resource, quantity
			self.quantity -= self.produced_quantity
			self.required_quantity -= self.produced_quantity * self.amount_used
			self.produced_quantity = 0

	def is_complete(self, building, dt):
		return (self.quantity < 1.0) | (self.required_quantity < 1.0)
