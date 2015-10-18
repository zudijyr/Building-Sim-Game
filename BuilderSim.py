#!/usr/bin/env python

import curses
import locale
import time
from models import Building

locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()
curses.initscr()  #s for screen
curses.noecho()
curses.cbreak()
curses.start_color()
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_RED)
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
	for y in xrange(1,19):
		w.addch(y,x,' ',curses.color_pair(1))
#w.bkgd(' ',curses.color_pair(1))    

w.refresh()

### add buildings
building1 = Building.cabbagePatch(2,2)
w.addch(building1.xPosition,building1.yPosition,building1.displayChar,curses.color_pair(1))
building2 = Building.fishingHole(5,5)
w.addch(building2.xPosition,building2.yPosition,building2.displayChar,curses.color_pair(1))
###

### move buildings
for i in range(0, 3):
	w.refresh()

	x = building1.xPosition
	y = building1.yPosition
	w.addch(y+1,x+1,building1.displayChar,curses.color_pair(1))
	w.addch(y,x,' ',curses.color_pair(1))
	building1.xPosition += 1
	building1.yPosition += 1

	x2 = building2.xPosition
	y2 = building2.yPosition
	w.addch(y2-1,x2+1,building2.displayChar,curses.color_pair(1))
	w.addch(y2,x2,' ',curses.color_pair(1))
	building2.xPosition += 1
	building2.yPosition -= 1

	time.sleep(1)
	w.refresh()
	

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
		w.addch(cursy,cursx,building1.displayChar,curses.color_pair(1))
		if(cursx > 1):
			cursy = cursy - 1
	elif c == ord('g'):
		w.addch(cursy,cursx,building2.displayChar,curses.color_pair(1))
	elif c == ord(' '):
		w.addch(cursy,cursx,building1.displayChar,curses.color_pair(1))
		#w.addch(cursy,cursx,' ',curses.color_pair(1))
	else:
		w.addch(cursy,cursx,c,curses.color_pair(2))
	w.move(cursy,cursx)
	w.refresh()

w.clear()
curses.nocbreak()
curses.echo()
curses.endwin()
