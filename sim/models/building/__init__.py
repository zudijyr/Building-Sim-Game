from sim import SimException
from sim.models.cargo_container import SlottedCargoContainer
from textwrap import indent
from uuid import uuid4


class BuildingException(SimException):
	pass


class Building:

	name = 'Unnamed'
	build_time = 1.0

	def __init__(self):
		self.resource_plants = []
		self.unit_factories = {}
		self.container = SlottedCargoContainer()
		self.building_id = uuid4()

	def add_resource_plant(self, resource_plant):
		self.resource_plants.append(resource_plant)

	def add_unit_factory(self, unit_factory):
		if unit_factory.product.name in self.unit_factories:
			message = "A factory for that unit has already been added"
			raise BuildingException(message)
		self.unit_factories[unit_factory.product.name] = unit_factory

	def receive_cargo(self, resource_type, quantity):
		return self.container.load_cargo(resource_type, quantity)

	def deliver_cargo(self, resource_type, quantity):
		return self.container.unload_cargo(resource_type, quantity)

	def produce_resources(self):
		[d.digest(self.container) for d in self.resource_plants]

	def build_unit(self, unit):
		if unit.name not in self.unit_factories:
			raise BuildingException("This building cannot build that unit")
		return self.unit_factories[unit.name].digest(self.container)

	def __repr__(self):
		lines = [
			'building_id: {}'.format(self.building_id),
			'name:        {}'.format(self.name),
			'container: \n{}'.format(indent(str(self.container), '  '))
			]
		for (index, resource_plant) in enumerate(self.resource_plants):
			lines.append('resource_plant {}:')
			lines.append(indent(str(resource_plant), '  '))
		for (index, unit_factory) in enumerate(self.unit_factories):
			lines.append('unit_factory {}:')
			lines.append(indent(str(unit_factory), '  '))
		return '\n'.join(lines)
