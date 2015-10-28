import curses

class Terrain:
    move_cost = 1
    name = 'base terrain'
    color = curses.COLOR_WHITE
    char_color = curses.COLOR_RED

    def display_terrain():
        print('Name : ', name)

class Forest(Terrain):
    name = 'forest'
    move_cost = 4
    color = curses.COLOR_MAGENTA
    char_color = curses.COLOR_BLACK

class Grass(Terrain):
    name = 'grass'
    move_cost = 2
    color = curses.COLOR_GREEN
    char_color = curses.COLOR_RED

class Water(Terrain):
    name = 'water'
    move_cost = 1
    color = curses.COLOR_BLUE
    char_color = curses.COLOR_MAGENTA

class Plains(Terrain):
    name = 'plains'
    move_cost = 2
    color = curses.COLOR_RED
    char_color = curses.COLOR_BLACK

#terrain1 = Plains()
#terrain2 = Grass()
#assert(terrain1.name == 'plains')
#assert(terrain1.move_cost == 2)
#assert(terrain2.name == 'grass')
#assert(terrain2.move_cost == 2)
