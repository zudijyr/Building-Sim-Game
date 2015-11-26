class TerrainImprovement:
	movement_factor = 1.0
	name = 'no improvement'
	can_build_iron_mine = False


class OreDeposit(TerrainImprovement):
	name = 'ore deposit'

	def __repr__(self):
		return self.name

	def __hash__(self):
		return self.name.__hash__()


class Road(TerrainImprovement):
	name = 'road'
	movement_factor = 2.0


class IronOreDeposit(OreDeposit):
	name = 'iron ore deposit'
	can_build_iron_mine = True
