#!/usr/bin/env python
import curses
import math
import time
import random

def init_curses(screen):
    '''
    load my preferred curses defaults
    '''

    curses.start_color()
    curses.noecho()
    curses.cbreak()
    screen.keypad(1)


def init_colors():
    '''
    load all xterm-256color colors
    '''
    for i in range(16, 256):
        curses.init_pair(i, i, 0)

def end_curses(screen):
    '''
    return screen to its normal state
    '''
    curses.nocbreak()
    screen.keypad(0)
    curses.echo()
    curses.endwin()

def draw_x_axis(y0, screen):
    '''
    draw the x axis at height y0
    '''
    for i in range(screen.getmaxyx()[1]):
        screen.addch(y0, i, "-" , curses.color_pair(0))

def draw_bar(y0, x0, y, screen, c="#", color=0):
    '''
    draw a bar starting at x0, y0 with height y on screen with char c in chosen color
    '''
    if y < 0:
        y = 0-y
        for i in range(y+1):
            screen.addch(min(y0+i, screen.getmaxyx()[0]), x0, c, curses.color_pair(color))
    else:
        for i in range(y+1):
            screen.addch(max(y0-i, 0), x0, c, curses.color_pair(color))

def draw_wide_bar(y0, x0, y, x, screen, c="#", color=0):
    '''
    draw a bar with width x
    '''
    for i in range(x):
        draw_bar(y0, min(x0+i, screen.getmaxyx()[1]), y, screen, c, color)

def color_select(n, threshold):
    '''
    given a value and 4-division threshold, return blue, green, yellow, or red
    '''
    if n < threshold[0]:
        return 33
    elif n < threshold[1]:
        return 83
    elif n < threshold[2]:
        return 119
    elif n < threshold[3]:
        return 227
    else:
        return 197


def draw_line(y0, x0, y1, x1, scr, c='.', color=255):
    x0, x1 = min(x0, x1), max(x0, x1)
    y0, y1 = min(y0, y1), max(y0, y1)
    if x0 == x1:
        return

    m = int((y1-y0) / (x1-x0))

    for i in range(0, x1-x0):
        scr.addch(y0 + (i*m), x0+ i, c, curses.color_pair(color))


if __name__ == '__main__':
    scr = curses.initscr()
    init_curses(scr)
    init_colors()

    maxy, maxx = scr.getmaxyx()
    oy = maxy/2
    ox = maxx/2

    draw_line(oy, ox, oy-10, ox-10, scr, "*", 197)

    scr.getch()

    end_curses(scr)
