import curses

class TerrainImprovement:
	movement_reduction = 1
	name = 'no improvement'
	display_char = ' '

	def display_terrain():
		print('Name : ', name)

class Road(TerrainImprovement):
	name = 'road'
	movement_reduction = 2
	display_char = '#'

