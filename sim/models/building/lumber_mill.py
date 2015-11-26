from sim.models.building import Building
from sim.models.producer_consumer import ResourcePlant
from sim.models.resource import Lumber, Wood


class LumberMill(Building):

	name = 'Lumber Mill'
	build_time = 10.0

	def __init__(self):
		super().__init__()
		self.container.add_resource_slot(Wood, 5)
		self.container.add_resource_slot(Lumber, 5)
		lumber_plant = ResourcePlant()
		lumber_plant.add_resource_requirement(Wood, 1)
		lumber_plant.add_resource_product(Lumber, 1)
		self.add_resource_plant(lumber_plant)
