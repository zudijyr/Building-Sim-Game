from sim.models.unit import Unit, UnitException
from sim.models.producer_consumer import Factory
from sim.models.building.dock import Dock
from sim.models.resource import Wood

class Ship(Unit):
	strength = 100
	movement_speed = 1.5
	name = 'Ship'

	def __init__(self):
		super().__init__()
		dock_factory = Factory()
		dock_factory.add_resource_requirement(Wood, 15)
		dock_factory.set_product(Dock)
		self.add_building_factory(dock_factory)

