from sim.models.building import Building
from sim.models.producer_consumer import ResourcePlant
from sim.models.resource import IronOre


class IronMine(Building):

	name = 'iron mine'
	build_time = 10.0

	def __init__(self):
		super().__init__()
		self.container.add_resource_slot(IronOre, 5)
		iron_ore_plant = ResourcePlant()
		iron_ore_plant.add_resource_product(IronOre, 1)
		self.add_resource_plant(iron_ore_plant)
