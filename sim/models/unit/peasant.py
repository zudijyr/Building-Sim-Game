from sim.models.unit import Unit
from sim.models.terrain import TerrainType
from sim.models.producer_consumer import Factory
from sim.models.building.cabbage_farm import CabbageFarm
from sim.models.building.iron_mine import IronMine
from sim.models.resource import Wood, Lumber


class Peasant(Unit):
	# TODO: make a way for units to drop off cargo at random places
	#       so they don't need to carry it all at once?
	strength = 30
	movement_speed = 1
	name = 'Peasant'
	moves_on_water = False

	def __init__(self):
		super().__init__()
		cabbage_farm_factory = Factory()
		cabbage_farm_factory.add_resource_requirement(Wood, 10)
		cabbage_farm_factory.set_product(CabbageFarm)
		self.add_building_factory(cabbage_farm_factory)
		self.add_harvestable_resource(Wood)
		self.add_carryable_resource(Wood)
		self.add_carryable_resource(Lumber)

		iron_mine_factory = Factory()
		iron_mine_factory.add_resource_requirement(Lumber, 10)
		iron_mine_factory.set_product(IronMine)
		self.add_building_factory(iron_mine_factory)

		self.traversable_terrain_types.add(TerrainType.land)
