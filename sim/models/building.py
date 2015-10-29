from sim.models import resource
from sim.models import unit
from sim.models.cargo_container import CargoContainer
from sim.models.producer_consumer import ProducerConsumer
from textwrap import indent

class Building:

    display_char = ''

    def __init__(self, x_position=0, y_position=0):
        self.digesters = []
        self.container = CargoContainer()
        self.x_position = x_position
        self.y_position = y_position
        self.setup()

    def setup(self):
        pass

    def receive_cargo(self, resource_type, quantity):
        capped_quantity = min(self.container.remaining_capacity(resource_type), quantity)
        self.container.load_cargo(resource_type, capped_quantity)
        return quantity - capped_quantity

    def deliver_cargo(self, resource_type, quantity):
        capped_quantity = min(self.container.current_load(resource_type), quantity)
        self.container.unload_cargo(resource_type, capped_quantity)
        return capped_quantity

    def operate(self):
        [ d.digest(self.container) for d in self.digesters ]

    def __repr__(self):
        lines = [
            'x_position:  {}'.format(self.x_position),
            'y_position:  {}'.format(self.y_position),
            'container: \n{}'.format(indent(self.container, '  '))
            ]
        for (index, digester) in enumerate(self.digesters):
            lines.append('digester {}:\n{}'.format(index, indent(digester, '  ')))

class CabbageFarm(Building):

    display_char = 'C'

    def setup(self):
        self.container.add_resource_slot(Cabbage, 5)
        self.container.add_resource_slot(Wood, 5)
        cabbage_producer = ProducerConsumer()
        cabbage_producer.add_resource_requirement(Wood, 1)
        cabbage_producer.add_resource_product(Cabbage, 1)
        self.digesters.append(cabbage_producer)

class Dock(Building):
    display_char = 'D'
    output_type = resource.Fish
    def setup(self):
        self.container.add_resource_slot(Fish, 5)
        fish_producer = ProducerConsumer()
        fish_producer.add_resource_product(Fish, 1)
        self.digesters.append(fish_producer)

class FishingHole(Building):
    display_char = 'F'

    def setup(self):
        self.container.add_resource_slot(Fish, 10)
        fish_producer = ProducerConsumer()
        fish_producer.add_resource_product(Fish, 3)
        self.digesters.append(fish_producer)

