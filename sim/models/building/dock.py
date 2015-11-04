from sim.models.producer_consumer import ResourcePlant
from sim.models.producer_consumer import Factory
from sim.models.building import Building, BuildingException
from sim.models.resource import Fish

class Dock(Building):

    display_char = 'D'
    name = 'Dock'

    def __init__(self):
        super().__init__()
        self.container.add_resource_slot(Fish, 5)
        fish_plant = ResourcePlant()
        fish_plant.add_resource_product(Fish, 1)
        self.add_resource_plant(fish_plant)

