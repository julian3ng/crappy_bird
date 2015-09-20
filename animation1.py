from grapher import *

scr = curses.initscr()
init_curses(scr)
init_colors()
def animation1():
    scr.nodelay(True)
    maxy, maxx = scr.getmaxyx()
    x_axis_height = maxy/2

    breaks = [2, 5, 7, 10]
    draw_x_axis(x_axis_height, scr)

    t = 0
    ch = scr.getch()
    while ch != curses.KEY_DOWN:
        ch = scr.getch()
        t += 1
        scr.clear()
        for i in range(1, maxx):
            y = int(10 * math.sin(0.111*(i-t)))
            if abs(y) < breaks[0]:
                draw_bar(x_axis_height, i, y, scr, '#', 19)
            elif abs(y) < breaks[1]:
                draw_bar(x_axis_height, i, y, scr, '#', 119)
            elif abs(y) < breaks[2]:
                draw_bar(x_axis_height, i, y, scr, '#', 227)
            else:
                draw_bar(x_axis_height, i, y, scr, '#', 197)

        scr.refresh()
        time.sleep(0.02)

animation1()
scr.nodelay(0)
end_curses(scr)
