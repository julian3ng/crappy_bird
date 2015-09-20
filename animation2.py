from grapher import *

scr = curses.initscr()
scr.nodelay(1)
init_curses(scr)
init_colors()
def animation2():
    maxy, maxx = scr.getmaxyx()
    y0 = maxy-1
    my_data=[]
    width=4

    while 1:
        if scr.getch() == curses.KEY_DOWN:
            break
        scr.clear()
        my_data.append(random.randint(0, maxy-1))
        if len(my_data) > (maxx-4)/4:
            my_data = my_data[-((maxx-4)/4):]
        for i, d in enumerate(my_data):

            draw_wide_bar(y0, i*width, d, width, scr, '#', color_select(d, [10, 20, 30, 40]))

        scr.refresh()
        time.sleep(0.2)

    scr.nodelay(0)
    scr.getch()
animation2()
end_curses(scr)
