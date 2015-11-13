from sim.models.unit import Unit, UnitException
from sim.models.producer_consumer import Factory
from sim.models.building.cabbage_farm import CabbageFarm
from sim.models.resource import Wood
from sim.models.terrain import Forest

class Peasant(Unit):
	strength = 25
	# Tiles per second
	movement_speed = 1
	name = 'Peasant'

	def __init__(self):
		super().__init__()
		cabbage_farm_factory = Factory()
		cabbage_farm_factory.add_resource_requirement(Wood, 10)
		cabbage_farm_factory.set_product(CabbageFarm)
		self.add_building_factory(cabbage_farm_factory)

