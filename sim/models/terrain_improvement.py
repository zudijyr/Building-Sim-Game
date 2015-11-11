import curses

class TerrainImprovement:
	movement_factor = 1.0
	name = 'no improvement'

class Road(TerrainImprovement):
	name = 'road'
	movement_factor = 2.0

