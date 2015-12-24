from sim.models.building import Building
from sim.models.producer_consumer import ResourcePlant
from sim.models.resource import Fish


class FishingHole(Building):

	name = 'Fishing Hole'
	build_time = 15.0

	def __init__(self):
		super().__init__()
		self.container.add_resource_slot(Fish, 10)
		fish_plant = ResourcePlant()
		fish_plant.add_resource_product(Fish, 3)
		self.add_resource_plant(fish_plant)
