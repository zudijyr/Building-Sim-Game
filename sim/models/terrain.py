import curses

BLUE    = (  0,   0, 255)
RED     = (255,   0,   0)
GREEN   = (  0, 255,   0)
WHITE   = (255, 255, 255)
BLACK   = (  0,   0,   0)
MAGENTA = (255,   0, 255)

class Terrain:
	movement_factor = 1.0
	name = 'base terrain'
	color = WHITE
	char_color = RED
	curses_color = curses.COLOR_WHITE
	curses_char_color = curses.COLOR_RED

	def display_terrain():
		print('Name : ', name)

class Forest(Terrain):
	name = 'forest'
	movement_factor = 0.25
	color = MAGENTA
	char_color = BLACK
	curses_color = curses.COLOR_MAGENTA
	curses_char_color = curses.COLOR_BLACK

class Grass(Terrain):
	name = 'grass'
	movement_factor = 0.5
	color = GREEN
	char_color = RED
	curses_color = curses.COLOR_GREEN
	curses_char_color = curses.COLOR_RED

class Water(Terrain):
	name = 'water'
	movement_factor = 1.0
	color = BLUE
	char_color = MAGENTA
	curses_color = curses.COLOR_BLUE
	curses_char_color = curses.COLOR_MAGENTA

class Plains(Terrain):
	name = 'plains'
	movement_factor = 0.75
	color = RED
	char_color = BLACK
	curses_color = curses.COLOR_RED
	curses_char_color = curses.COLOR_BLACK

