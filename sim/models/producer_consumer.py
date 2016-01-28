from sim import SimException


class ProducerConsumerException(SimException):
	pass


class ProducerConsumer:

	def __init__(self):
		self.resource_requirements = {}
		self.required_resource_list = []

	def __repr__(self):
		lines = []
		for key in self.resource_requirements.keys():
			requirement = self.resource_requirements[key]
			lines.append('consumes {}:'.format(key))
			lines.append('  type:     {}'.format(requirement['type']))
			lines.append('  load:     {}\n'.format(requirement['load']))
		return '\n'.join(lines)

	def add_resource_requirement(self, input_type, input_load):
		if input_type.name in self.resource_requirements:
			message = "A resource requirement of that type has"
			message += " already been added"
			raise ProducerConsumerException(message)
		self.resource_requirements[input_type.name] = {
			'load': input_load,
			'type': input_type,
			}
		self.required_resource_list.append(input_type)

	def can_consume(self, cargo_container):
		for requirement in self.resource_requirements.values():
			if not cargo_container.can_hold_cargo(requirement['type']):
				return False
			current_load = cargo_container.current_load(requirement['type'])
			if current_load < requirement['load']:
				return False
		return True

	def digest(self, cargo_container):
		message = "This method must be overridden in a derived class"
		raise ProducerConsumerException(message)


class ResourcePlant(ProducerConsumer):

	def __init__(self):
		super().__init__()
		self.resource_products = {}

	def __repr__(self):
		lines = []
		for key in self.resource_products.keys():
			product = self.resource_products[key]
			lines.append('produces {}:'.format(key))
			lines.append('  type:     {}'.format(product['type']))
			lines.append('  load:     {}'.format(product['load']))
		return super().__repr__() + '\n'.join(lines)

	def add_resource_product(self, output_type, output_load):
		if output_type.name in self.resource_products:
			message = "A resource product of that type has already been added"
			raise ProducerConsumerException(message)
		self.resource_products[output_type.name] = {
			'load': output_load,
			'type': output_type,
			}

	def can_produce(self, cargo_container):
		for requirement in self.resource_products.values():
			if not cargo_container.can_hold_cargo(requirement['type']):
				return False
			capacity = cargo_container.remaining_capacity(requirement['type'])
			if capacity < requirement['load']:
				return False
		return True

	def digest(self, cargo_container):
		can_consume = self.can_consume(cargo_container)
		can_produce = self.can_produce(cargo_container)
		if not can_consume or not can_produce:
			return
		for requirement in self.resource_requirements.values():
			cargo_container.unload_cargo(
				requirement['type'],
				requirement['load'],
				)
		for requirement in self.resource_products.values():
			cargo_container.load_cargo(
				requirement['type'],
				requirement['load'],
				)
		return None


class Factory(ProducerConsumer):

	def __init__(self):
		super().__init__()
		self.product = None

	def __repr__(self):
		lines = []
		lines.append('produces {}:'.format(self.product.name))
		return super().__repr__() + '\n'.join(lines)

	def set_product(self, product):
		if self.product is not None:
			message = "The product for this factory has already been set"
			raise ProducerConsumerException(message)
		self.product = product

	def digest(self, cargo_container):
		if not self.can_consume(cargo_container):
			return
		for requirement in self.resource_requirements.values():
			cargo_container.unload_cargo(
				requirement['type'],
				requirement['load'],
				)
		return self.product()
