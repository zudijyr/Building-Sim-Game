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
            lines.append('  capacity: {}'.format(self.cargo_slots[key]['capacity']))
            lines.append('  load:     {}'.format(self.cargo_slots[key]['load']))
            lines.append('  type:     {}'.format(self.cargo_slots[key]['type']))
        return '\n'.join(lines)

    def add_resource_slot(self, input_type, input_capacity):
        if input_type.name in self.cargo_slots:
            raise CargoContainerException("An input slot of that resource type has already been added")
        self.cargo_slots[input_type.name] = {
            'capacity' : input_capacity,
            'load'     : 0,
            'type'     : input_type,
            }

    def can_load_cargo(self, resource_type, quantity):
        if resource_type.name not in self.cargo_slots:
            return False
        return quantity <= self.remaining_capacity(resource_type)

    def can_unload_cargo(self, resource_type, quantity):
        if resource_type.name not in self.cargo_slots:
            return False
        return self.current_load(resource_type) - quantity >= 0

    def load_cargo(self, resource_type, quantity):
        if not self.can_load_cargo(resource_type, quantity):
            raise CargoContainerException("Cannot load resource {}".format(resource_type))
        self.cargo_slots[resource_type.name]['load'] += quantity

    def unload_cargo(self, resource_type, quantity):
        if not self.can_unload_cargo(resource_type, quantity):
            raise CargoContainerException("Cannot unload resource {}".format(resource_type))
        self.cargo_slots[resource_type.name]['load'] -= quantity

    def remaining_capacity(self, resource_type):
        if resource_type.name not in self.cargo_slots:
            raise CargoContainerException("A cargo slot of that resource type has not been added")
        slot = self.cargo_slots[resource_type.name]
        return slot['capacity'] - slot['load']

    def current_load(self, resource_type):
        if resource_type.name not in self.cargo_slots:
            raise CargoContainerException("A cargo slot of that resource type has not been added")
        slot = self.cargo_slots[resource_type.name]
        return slot['load']
