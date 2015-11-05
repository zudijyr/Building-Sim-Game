class ProducerConsumerException(Exception):
	def __init__(self, message):
		self.message = message
	def __str__(self):
		return self.message

class ProducerConsumer:

	def __init__(self):
		self.resource_requirements = {}

	def __repr__(self):
		lines = []
		for key in self.resource_requirements.keys():
			lines.append('consumes {}:'.format(key))
			lines.append('  type:     {}'.format(self.resource_requirements[key]['type']))
			lines.append('  load:     {}'.format(self.resource_requirements[key]['load']))
		return '\n'.join(lines)

	def add_resource_requirement(self, input_type, input_load):
		if input_type.name in self.resource_requirements:
			raise ProducerConsumerException("A resource requirement of that type has already been added")
		self.resource_requirements[input_type.name] = {
			'load'     : input_load,
			'type'     : input_type,
			}

	def can_consume(self, cargo_container):
		for requirement in self.resource_requirements.values():
			if not cargo_container.can_hold_cargo(requirement['type']):
				return False
			if cargo_container.current_load(requirement['type']) < requirement['load']:
				return False
		return True

	def digest(self, cargo_container):
		raise ProducerConsumerException("This method must be overridden in a derived class")

class ResourcePlant(ProducerConsumer):

	def __init__(self):
		super().__init__()
		self.resource_products = {}

	def __repr__(self):
		lines = []
		for key in self.resource_products.keys():
			lines.append('produces {}:'.format(key))
			lines.append('  type:     {}'.format(self.resource_products[key]['type']))
			lines.append('  load:     {}'.format(self.resource_products[key]['load']))
		return super().__repr__() + '\n'.join(lines)

	def add_resource_product(self, output_type, output_load):
		if output_type.name in self.resource_products:
			raise ProducerConsumerException("A resource product of that type has already been added")
		self.resource_products[output_type.name] = {
			'load'     : output_load,
			'type'     : output_type,
			}

	def can_produce(self, cargo_container):
		for requirement in self.resource_products.values():
			if not cargo_container.can_hold_cargo(requirement['type']):
				return False
			if cargo_container.remaining_capacity(requirement['type']) < requirement['load']:
				return False
		return True

	def digest(self, cargo_container):
		if not self.can_consume(cargo_container) or not self.can_produce(cargo_container):
			return
		for requirement in self.resource_requirements.values():
			cargo_container.unload_cargo(requirement['type'], requirement['load'])
		for requirement in self.resource_products.values():
			cargo_container.load_cargo(requirement['type'], requirement['load'])
		return None

class Factory(ProducerConsumer):

	def __init__(self):
		super().__init__()
		self.product = None

	def __repr__(self):
		lines = []
		for key in self.resource_products.keys():
			lines.append('produces {}:'.format(key))
			lines.append('  type:     {}'.format(self.resource_products[key]['type']))
			lines.append('  load:     {}'.format(self.resource_products[key]['load']))
		return super().__repr__() + '\n'.join(lines)

	def set_product(self, product):
		if self.product is not None:
			raise ProducerConsumerException("The product for this factory has already been set")
		self.product = product

	def digest(self, cargo_container):
		if not self.can_consume(cargo_container):
			return
		for requirement in self.resource_requirements.values():
			cargo_container.unload_cargo(requirement['type'], requirement['load'])
		return self.product()
