#!/usr/bin/env python

import curses
import locale
import time
from models import unit
from models import building
from models import terrain

locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()
curses.initscr()  #s for screen
curses.noecho()
curses.cbreak()
curses.start_color()
curses.init_pair(1, curses.COLOR_RED, terrain.Hill.color)
curses.init_pair(2, curses.COLOR_BLUE, terrain.Plains.color)
curses.init_pair(3, curses.COLOR_RED, terrain.Terrain.color)
curses.init_pair(4, curses.COLOR_MAGENTA, terrain.Water.color)
w = curses.newwin(20,20,0,0)
w.keypad(1)
w.border(0)
###
#w.addstr(1, 1, '1')
#w.addstr(1, 2, u"\U0001F37A".encode('utf-8'))
#w.addstr(1, 3, "wtf")
#w.addstr(2, 2, u"\U0001F37A".encode('utf-8'))
#w.addstr(2, 3, u"\U0001F37A".encode('utf-8'))
###

for x in xrange(1,19):
	for y in xrange(1,10):
		w.addch(y,x,' ',curses.color_pair(1))
	for y in xrange(10,11):
		w.addch(y,x,' ',curses.color_pair(3))
	for y in xrange(11,19):
		w.addch(y,x,' ',curses.color_pair(4))
#w.bkgd(' ',curses.color_pair(1))    

w.refresh()

### add units
unit1 = unit.Peasant(2,2, "null")
w.addch(unit1.y_position,unit1.x_position,unit1.display_char,curses.color_pair(1))
unit2 = unit.Ship(5,15, "null")
w.addch(unit2.y_position,unit2.x_position,unit2.display_char,curses.color_pair(4))
###

### add buildings
building1 = building.FishingHole(8,12)
w.addch(building1.y_position,building1.x_position,building1.display_char,curses.color_pair(4))

### move units
for i in range(0, 3):
	w.refresh()

	x = unit1.x_position
	y = unit1.y_position
	w.addch(y+1,x+1,unit1.display_char,curses.color_pair(1))
	w.addch(y,x,' ',curses.color_pair(1))
	unit1.x_position += 1
	unit1.y_position += 1

	x2 = unit2.x_position
	y2 = unit2.y_position
	w.addch(y2-1,x2+1,unit2.display_char,curses.color_pair(4))
	w.addch(y2,x2,' ',curses.color_pair(4))
	unit2.x_position += 1
	unit2.y_position -= 1

	time.sleep(1)
	w.refresh()

### get fish
building1.input_load = 5
building1.produce()
assert(building1.output_load == 1)
building1.load_building_cargo_into_unit(unit1)
assert(unit1.cargo_load == 1)


go = 1
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
		w.addch(cursy,cursx,building1.display_char,curses.color_pair(1))
		#w.addch(cursy,cursx,' ',curses.color_pair(1))
	else:
		w.addch(cursy,cursx,c,curses.color_pair(2))
	w.move(cursy,cursx)
	w.refresh()

w.clear()
curses.nocbreak()
curses.echo()
curses.endwin()
