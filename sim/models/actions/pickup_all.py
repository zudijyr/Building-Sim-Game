from sim.models.actions.pickup import Pickup
import math

class PickupAll(Pickup):

	def setup(self, unit):
		for resource in unit.carryable_resources:
			Pickup.setup(self, resource, unit.container.remaining_capacity(resource))
