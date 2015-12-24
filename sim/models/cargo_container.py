from sim import SimException


class CargoContainerException(SimException):
	pass


class CargoContainer:

	def __init__(self):
		self.cargo_slots = {}

	def __repr__(self):
		lines = []
		for (name, slot) in self.cargo_slots.items():
			lines.append('{} load :{:.2f}'.format(name, slot['load']))
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
		message = "This method should be overloaded in derived class"
		raise CargoContainerException(message)

	def remaining_capacity(self, resource_type):
		message = "This method should be overloaded in derived class"
		raise CargoContainerException(message)

	def current_load(self, resource_type):
		message = "This method should be overloaded in derived class"
		raise CargoContainerException(message)

	def get_slot(self, resource_type):
		message = "This method should be overloaded in derived class"
		raise CargoContainerException(message)


class MixedCargoContainer(CargoContainer):

	def __init__(self):
		super().__init__()
		self.weight_capacity = 0

	def __repr__(self):
		return '\n'.join([
			'weight_capacity: {}'.format(self.weight_capacity),
			'current_weight: {:.2f}'.format(self.get_current_weight()),
			super().__repr__(),
			])

	def get_slot(self, resource_type):
		return self.cargo_slots.setdefault(
			resource_type.name,
			{'load': 0, 'type': resource_type}
			)

	def can_hold_cargo(self, resource_type):
		return True

	def get_current_weight(self):
		current_weight = 0
		for slot in self.cargo_slots.values():
			current_weight += slot['load'] * slot['type'].weight
		return current_weight

	def set_weight_capacity(self, weight_capacity):
		if weight_capacity <= 0:
			message = "Weight capacity must be greater than 0"
			raise CargoContainerException(message)
		if weight_capacity <= self.get_current_weight():
			message = "Capacity must be greater than or equal to"
			message += " the current weight"
			raise CargoContainerException(message)
		self.weight_capacity = weight_capacity

	def remaining_capacity(self, resource_type):
		self.get_slot(resource_type)
		remaining_weight = self.weight_capacity - self.get_current_weight()
		return remaining_weight // resource_type.weight

	def current_load(self, resource_type):
		slot = self.get_slot(resource_type)
		return slot['load']


class SlottedCargoContainer(CargoContainer):

	def __repr__(self):
		lines = []
		for (name, slot) in self.cargo_slots.items():
			lines.append('{} capacity {:.2f}:'.format(name, slot['capacity']))
		return '\n'.join(lines + [super().__repr__()])

	def get_slot(self, resource_type):
		if resource_type.name not in self.cargo_slots:
			message = "A cargo slot of that type has not been added: "
			message += str(resource_type)
			raise CargoContainerException(message)
		return self.cargo_slots[resource_type.name]

	def add_resource_slot(self, input_type, input_capacity):
		if input_type.name in self.cargo_slots:
			message = "An input slot of that resource type has "
			message += "already been added"
			raise CargoContainerException(message)
		self.cargo_slots[input_type.name] = {
			'capacity': input_capacity,
			'load': 0,
			'type': input_type,
			}

	def can_hold_cargo(self, resource_type):
		return resource_type.name in self.cargo_slots

	def remaining_capacity(self, resource_type):
		slot = self.get_slot(resource_type)
		return slot['capacity'] - slot['load']

	def current_load(self, resource_type):
		slot = self.get_slot(resource_type)
		return slot['load']
