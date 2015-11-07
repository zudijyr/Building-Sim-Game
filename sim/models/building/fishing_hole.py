from sim.models.producer_consumer import ResourcePlant
from sim.models.building import Building, BuildingException
from sim.models.resource import Fish

class FishingHole(Building):

    display_char = 'F'
    name = 'Fishing Hole'

    def __init__(self):
        super().__init__()
        self.container.add_resource_slot(Fish, 10)
        fish_plant = ResourcePlant()
        fish_plant.add_resource_product(Fish, 3)
        self.add_resource_plant(fish_plant)

