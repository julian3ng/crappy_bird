#!/usr/bin/env python
import curses
from math import *
import time
import sys
import parser
import argparse

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

def draw_x_axis(y, screen):
    '''
    draw x axis at height y
    '''
    screen.hline(y, 0, '-', screen.getmaxyx()[1])

def draw_y_axis(x, screen):
    '''
    draw y axis at location x
    '''
    screen.vline(0, x, '|', screen.getmaxyx()[0])

def draw_origin(y, x, screen):
    '''
    mark the origin down
    '''
    screen.addch(y, x, '+')

def plot_point(y, x, screen, c='.', color=255):
    '''
    plots (y, x) where y and x are coordinates with respect to the axes
    '''
    max_y, max_x = screen.getmaxyx()
    screen.addch(max_y-(y+int(max_y/2)), x+(int(max_x/2)), c, curses.color_pair(color))

def plot_abs_point(y, x, screen, c='.', color=255):
    screen.addch(y, x, c, curses.color_pair(color))

if __name__ == '__main__':
    scr = curses.initscr()
    init_curses(scr)
    init_colors()

    max_y, max_x = scr.getmaxyx()
    oy = int(max_y/2)
    ox = int(max_x/2)
    eq = sys.argv[1]
    code = parser.expr(eq).compile()


    t = -ox
    while t <= ox-1:
        scr.clear()
        draw_x_axis(oy, scr)
        draw_y_axis(ox, scr)
        draw_origin(oy, ox, scr)

        for x in range(-ox, t):
            try:
                y = int(eval(code))
                plot_point(y, x, scr, '.', 199)
                scr.addstr(0, 0, "("+str(x)+", "+str(y)+")", curses.color_pair(51))
            except ValueError:
                plot_abs_point(0, ox, scr, '|', 199)
                scr.addstr(0, 0, "(ValueError, "+str(x)+")", curses.color_pair(199))
            except:
                plot_abs_point(0, ox, scr, '|', 199)
                scr.addstr(0, 0, "("+str(y)+", "+str(x)+")", curses.color_pair(199))

        plot_point(0, t, scr, '|', 199)
        t+=1
        time.sleep(0.1)
        scr.refresh()


    scr.getch()
    end_curses(scr)
