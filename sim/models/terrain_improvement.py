class TerrainImprovement:
	movement_factor = 1.0
	name = 'no improvement'
	can_build_iron_mine = False

class OreDeposit(TerrainImprovement):
	name = 'ore deposit'

class Road(TerrainImprovement):
	name = 'road'
	movement_factor = 2.0

class IronOreDeposit(OreDeposit):
	name = 'iron ore deposit'
	can_build_iron_mine = True
