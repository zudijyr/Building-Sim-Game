#!/usr/bin/env python

import curses
import locale
import time
import resource
from models import resource
from models import terrain
from models import building
from models import unit

locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()
curses.initscr()  #s for screen
curses.noecho()
curses.cbreak()
curses.start_color()
w = curses.newwin(20,20,0,0)
w.keypad(1)
w.border(0)

for x in xrange(1,19):
	for y in xrange(1,19):
		w.addch(y,x,' ',terrain.Grass.color_pair)
	for y in xrange(10,11):
		w.addch(y,x,' ',terrain.Terrain.color_pair)
	for y in xrange(11,19):
		w.addch(y,x,' ',terrain.Water.color_pair)

w.refresh()

### add units
unit1 = unit.Peasant(2,2, resource.NullResource)
w.addch(unit1.y_position,unit1.x_position,unit1.display_char,terrain.Grass.color_pair)
unit2 = unit.Ship(8,12, resource.NullResource)
w.addch(unit2.y_position,unit2.x_position,unit2.display_char,terrain.Water.color_pair)
###

### add buildings
building1 = building.FishingHole(5,15)
building2 = building.Dock(6,10)
building3 = building.Dock(6,11)
building4 = building.Dock(6,12)

w.addch(building1.y_position,building1.x_position,building1.display_char,terrain.Water.color_pair)
w.addch(building2.y_position,building2.x_position,building2.display_char,terrain.Terrain.color_pair)
w.addch(building3.y_position,building3.x_position,building3.display_char,terrain.Water.color_pair)
w.addch(building4.y_position,building4.x_position,building4.display_char,terrain.Water.color_pair)

w.refresh()

### move units
for i in range(0, 3):

	unit1.move_unit(w, 1,1, terrain.Grass)
	unit2.move_unit(w,-1,1, terrain.Water)
	time.sleep(1)
	w.refresh()

### get fish
building1.input_load = 5
building1.produce()
building1.produce()
assert(building1.output_load == 2)
building1.load_building_cargo_into_unit(unit1)
assert(unit1.cargo_load == 2)

### go to dock
for i in range(0, 3):
	w.refresh()

	unit2.move_unit(w,0,-1, terrain.Water)

	time.sleep(1)
	w.refresh()

cursx = 1
cursy = 1
w.move(cursy,cursx)
while 1:
	c = w.getch()
	if c == ord('q'):
		break
	elif c == curses.KEY_RIGHT:
		if(cursx < 19):
			cursx = cursx + 1
	elif c == curses.KEY_LEFT:
		if(cursx > 1):
			cursx = cursx - 1
	elif c == curses.KEY_DOWN:
		if(cursy < 19):
			cursy = cursy + 1
	elif c == curses.KEY_UP:
		if(cursy > 1):
			cursy = cursy - 1
	elif c == ord('d'):
		w.addch(cursy,cursx,building1.display_char,curses.color_pair(1))
		if(cursx > 1):
			cursy = cursy - 1
	elif c == ord(' '):
		w.addch(cursy,cursx,' ',curses.color_pair(1))
	else:
		w.addch(cursy,cursx,c,curses.color_pair(2))
	w.move(cursy,cursx)
	w.refresh()

w.clear()
curses.nocbreak()
curses.echo()
curses.endwin()
