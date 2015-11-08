class CargoContainerException(Exception):
	def __init__(self, message):
		self.message = message
	def __str__(self):
		return self.message

class CargoContainer:

	def __init__(self):
		self.cargo_slots = {}

	def __repr__(self):
		lines = []
		for key in self.cargo_slots.keys():
			lines.append('{}:'.format(key))
			slot = self.cargo_slots[key]
			[ lines.append('  {}: {}'.format(k, slot[k])) for k in slot.keys() ]
		return '\n'.join(lines)

	def load_cargo(self, resource_type, quantity):
		capacity = self.remaining_capacity(resource_type)
		capped_quantity = min(capacity, quantity)
		self.cargo_slots[resource_type.name]['load'] += capped_quantity
		return quantity - capped_quantity

	def unload_cargo(self, resource_type, quantity):
		load = self.current_load(resource_type)
		capped_quantity = min(load, quantity)
		self.cargo_slots[resource_type.name]['load'] -= capped_quantity
		return capped_quantity

	def can_hold_cargo(self, resource_type):
		raise CargoContainerException("This method should be overloaded in derived class")

	def remaining_capacity(self, resource_type):
		raise CargoContainerException("This method should be overloaded in derived class")

	def current_load(self, resource_type):
		raise CargoContainerException("This method should be overloaded in derived class")

	def get_slot(self, resource_type):
		raise CargoContainerException("This method should be overloaded in derived class")

class MixedCargoContainer(CargoContainer):

	def __init__(self):
		super().__init__()
		self.weight_capacity = 0

	def __repr__(self):
		return '\n'.join([
			'weight_capacity: {}'.format(self.weight_capacity),
			'current_weight: {}'.format(self.get_current_weight()),
			super().__repr__(),
			])

	def get_slot(self, resource_type):
		return self.cargo_slots.setdefault(resource_type.name, { 'load':0, 'type':resource_type })

	def can_hold_cargo(self, resource_type):
		return True

	def get_current_weight(self):
		current_weight = 0
		for slot in self.cargo_slots.values():
			current_weight += slot['load'] * slot['type'].weight
		return current_weight

	def set_weight_capacity(self, weight_capacity):
		if weight_capacity <= 0:
			raise CargoContainerException("Weight capacity must be greater than 0")
		if weight_capacity <= self.get_current_weight():
			message = "Weight capacity must be greater than or equal to the current weight"
			raise CargoContainerException(message)
		self.weight_capacity = weight_capacity

	def remaining_capacity(self, resource_type):
		slot = self.get_slot(resource_type)
		return (self.weight_capacity - self.get_current_weight()) // resource_type.weight

	def current_load(self, resource_type):
		slot = self.get_slot(resource_type)
		return slot['load']

class SlottedCargoContainer(CargoContainer):

	def get_slot(self, resource_type):
		if resource_type.name not in self.cargo_slots:
			message = "A cargo slot of that type has not been added: {}".format(resource_type)
			raise CargoContainerException(message)
		return self.cargo_slots[resource_type.name]

	def add_resource_slot(self, input_type, input_capacity):
		if input_type.name in self.cargo_slots:
			raise CargoContainerException("An input slot of that resource type has already been added")
		self.cargo_slots[input_type.name] = {
			'capacity' : input_capacity,
			'load'     : 0,
			'type'     : input_type,
			}

	def can_hold_cargo(self, resource_type):
		return resource_type.name in self.cargo_slots

	def remaining_capacity(self, resource_type):
		slot = self.get_slot(resource_type)
		return slot['capacity'] - slot['load']

	def current_load(self, resource_type):
		slot = self.get_slot(resource_type)
		return slot['load']

