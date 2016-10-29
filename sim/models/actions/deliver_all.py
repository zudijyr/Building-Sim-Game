from sim.models.actions.deliver import Deliver
import math

class DeliverAll(Deliver):

	def setup(self, unit):
		for resource in unit.carryable_resources:
			Deliver.setup(self, resource, unit.container.current_load(resource))
