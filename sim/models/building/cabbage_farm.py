from sim.models.building import Building
from sim.models.producer_consumer import ResourcePlant
from sim.models.resource import Cabbage, Wood


class CabbageFarm(Building):

	name = 'Cabbage Farm'
	build_time = 10.0

	def __init__(self):
		super().__init__()
		self.container.add_resource_slot(Cabbage, 5)
		self.container.add_resource_slot(Wood, 5)
		cabbage_plant = ResourcePlant()
		cabbage_plant.add_resource_requirement(Wood, 1)
		cabbage_plant.add_resource_product(Cabbage, 1)
		self.add_resource_plant(cabbage_plant)
