from sim.models.unit import Unit, UnitException
from sim.models.producer_consumer import Factory
from sim.models.building.cabbage_farm import CabbageFarm
from sim.models.resource import Wood
from sim.models.terrain import Forest

class Peasant(Unit):
	strength = 25
	movement_speed = 25
	display_char = 'P'
	name = 'Peasant'

	def __init__(self):
		super().__init__()
		cabbage_farm_factory = Factory()
		cabbage_farm_factory.add_resource_requirement(Wood, 10)
		cabbage_farm_factory.set_product(CabbageFarm)
		self.add_building_factory(cabbage_farm_factory)

	def chop_wood(self):
		current_terrain = self.tile_map.get_terrain_under_unit(self)
		if current_terrain != Forest:
			return
		if self.container.remaining_capacity(Wood) <= 0:
			return
		self.moves_remaining -= 1
		self.container.load_cargo(Wood, 1)

