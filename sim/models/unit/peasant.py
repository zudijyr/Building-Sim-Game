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

	def can_chop_wood(self):
		# TODO: See if there is any wood left on the tile
		if self.tile_map.get_tile_under_unit(self).terrain != Forest:
			return False
		if self.container.remaining_capacity(Wood) <= 0:
			return False
		return True

	def check_for_wood_to_chop(self, dt, quantity=1):
		print("checking for wood")
		if not self.can_chop_wood():
			return
		print("Can Chop!")
		capped_quantity = min(quantity, self.container.remaining_capacity(Wood))
		self.add_immediate_action(self.chop_wood, quantity=quantity)

	def chop_wood(self, dt, quantity=1):
		"""
		It might be useful to have a wood choping rate or something so dt is
		actually meaningful in this context
		"""
		print("chopping wood")
		if not self.can_chop_wood():
			return
		self.container.load_cargo(Wood, 1)
		if quantity > 1:
			self.add_immediate_action(self.chop_wood, quantity=quantity - 1)

	def attempt_to_build_cabbage_farm(self, dt):
		print("attempting to build cabbage farm")
		print("cabbage factory: {}".format(self.building_factories[CabbageFarm.name]))
		if self.can_construct_building(CabbageFarm):
			print("Can build!")
			self.add_immediate_action(self.build_cabbage_farm)

	def build_cabbage_farm(self, dt):
		print("building cabbage farm")
		cabbage_farm = self.construct_building(CabbageFarm)
		(x, y) = self.tile_map.get_unit_position(self)
		self.tile_map.place_building(cabbage_farm, x, y)

