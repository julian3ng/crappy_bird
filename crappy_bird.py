#!/usr/bin/env python

#####################################################
# Author: Julian Eng                                #
# NetID: jje59                                      #
# School: Cornell University College of Engineering #
# Date: 9-19-15                                     #
# Flappy Bird clone                                 #
# This was just for fun, made in the last couple of #
#  hours in the hackathon.                          #
#####################################################

import curses
import curses.ascii
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

def draw_bar(y0, x0, y, screen, c="#", color=0):
    '''
    draw a bar starting at x0, y0 with height y on screen with string in chosen color
    '''
    if y < 0:
        y = 0-y
        for i in range(y+1):
            screen.addstr(min(y0+i, screen.getmaxyx()[0]), x0, c, curses.color_pair(color))
    else:
        for i in range(y+1):
            screen.addstr(max(y0-i, 0), x0, c, curses.color_pair(color))

def draw_wide_bar(y0, x0, y, x, screen, c="#", color=0):
    '''
    draw a bar with width x
    '''
    for i in range(x):
        draw_bar(y0, (x0+i)%(screen.getmaxyx()[1]-1), y, screen, c, color)

def draw_character(y, x, screen, score, c='>', color=82):
    screen.addstr(y, x, c, curses.color_pair(color))


def apply_velocity(vel_y, y):
    return y + vel_y

def apply_gravity(vel_y, acc_y):
    return vel_y + acc_y

def death(y, x, score=0):
    death_message = "TERMINATED"
    continue_message = "Press any key to continue..."
    score_message = "SCORE: " + str(score)
    scr.clear()
    scr.addstr(y, x-int(len(death_message)/2), death_message, curses.color_pair(197))
    scr.addstr(y+1, x-int(len(continue_message)/2), continue_message, curses.color_pair(50))
    scr.nodelay(0)
    scr.getch()
    scr.clear()
    scr.addstr(y, x-int(len(score_message)/2), score_message, curses.color_pair(47))
    scr.getch()
    end_curses(scr)
    with open('scores.txt', 'a') as out:
        out.write(str(score))


def pause():
    scr.nodelay(0)
    scr.getch()
    scr.nodelay(1)

if __name__ == '__main__':
    scr = curses.initscr()
    init_curses(scr)
    init_colors()
    scr.nodelay(1)

    max_y, max_x = scr.getmaxyx()
    max_x = max_x - 1
    oy = int(max_y/2)
    ox = int(max_x/2)
    y = int(max_y/2)
    x = int(max_x/3)
    t = 0
    time_inc = 0.07
    vel_y = 0
    acc_y = 0.5
    flap_vel = -2
    obstacle_char = '#'
    in_char = -1
    top_bound = int(max_y*2/5)
    bottom_bound = int(max_y*4/5)
    gap_width = 10
    obstacles = []
    spacing = 25

    for i in range(0, 9):
        obstacles.append([i*spacing, int(max_y/2)+10, int(max_y/2)-10])

    while 1:
        try:
            scr.clear()
            #jump!
            in_char = scr.getch()
            if (in_char != -1):
                vel_y = flap_vel

            #update vars
            vel_y = apply_gravity(vel_y, acc_y)
            y = apply_velocity(vel_y, y)
            t += 1
            #out of bounds
            if (y >= max_y) or (y <= 0):
                death(oy, ox, t)
                break
            else:
                #keep going
                draw_character(int(y), int(max_x / 3), scr, t)

                if t%100 == 0:
                    gap_width -= 1
                if gap_width < 5:
                    gap_width = 9

                for i,x in enumerate(obstacles[-8:]):
                    gap_bottom = random.randint(top_bound, bottom_bound)
                    gap_top = gap_bottom - random.randint(gap_width, gap_width*2)
                    if x[1] == 0:
                        x[1] = gap_bottom
                        x[2] = gap_top
                    # draw bottom bar
                    draw_wide_bar(max_y-1, x[0] - t, max_y-1-x[1], 4, scr, obstacle_char, 197)
                    # draw top bar
                    draw_wide_bar(x[2], x[0] - t, x[2], 4, scr, obstacle_char, 197)

                scr.addstr(max_y-3, max_x-len(str(t))-3, str(t), curses.color_pair(51))

                # collision check
                if (scr.inch(int(y), int(max_x / 3)) & 0b11111111 == ord(obstacle_char)): # last 8 digits are the char
                    death(oy, ox, t)
                    break
                if (scr.instr(2, 0, 5) == "#### "):
                    obstacles.append([obstacles[-1][0]+spacing, 0, 0])
                if (scr.instr(2, max_x-6, 5) == "#### "):
                    del(obstacles[0])
                scr.refresh()
                time_inc = max(0.07, 2-math.log(t+5))
                time.sleep(time_inc)
        except KeyboardInterrupt:
            death(oy, ox, t)
            break
