#
#   Authors: Steven Freed, Samuel Jefferson, Anthony Pensak
#

import forward_astar as fa
import adaptive_astar as aa
import numpy as np
import pygame as pg
import sys

width = 768
height = 768

black = [0, 0, 0]
white = [255, 255, 255]
red = [255, 0, 0]
dark_red = [200, 0,0]
green = [0, 255, 0]
dark_green = [0, 200, 0]
blue = [0, 0, 255]
dark_blue = [0, 0, 200]
yellow = [255, 255, 0]
orange = [255, 165, 0]
grey = gray = [100, 100, 100]

def remove_bool(path):
    newpath = []
    for item in path:
        point, bool = item
        newpath.append(point)
    return newpath

def add_bool(path):
    newpath = []
    for point in path:
        newpath.append((point, True))
    return newpath

def optimizePath(final_path):
    list=final_path.copy()
    x=range(len(list))
    for i in x:
        a1=i+1#
        if a1 < len(list):
            z=range(a1,len(list))
            for j in z:
                if (i in x):
                    if (j in z):
                        if (list[i]==list[j]):
                            for y in range(i,j):
                                del(list[i])
                                x=range(len(list))
                                z=range(len(list))
    for x in list:
        if list.count(x)>=2:
            list=optimizePath(list)

    q=range(len(list))
    for i in q:
        a1=i+1#
        if a1 < len(list):
            z=range(a1,len(list))
            for j in z:
                if (i in q):
                    if (j in z):
                        x,y=list[i]
                        hf=x,y+1#used for checking for Circuit on the horizontal, forward
                        vf=x+1,y#used for checking for Circuits on the veritcal,forward
                        hb=x,y-1#horiz,Backward
                        vb=x-1,y#vert,Backward
                        if list[j]==hf or list[j]==vf or list[j]==hb or list[j]==vb:
                            if list.index(list[j]) != (list.index(list[i])+1):
                                for y in range(i+1,j):
                                    del(list[i+1])
                                    q=range(len(list))
                                    z=range(len(list))
    return list

def set_girth(dim):
    rows, cols = dim
    if rows < 50:
        return 2
    else:
        return 1

def make_env(str, dim):
    x_min = 0
    y_min = 0
    rows, cols = dim
    print(rows, cols)
    env = np.zeros(rows*cols).reshape(rows,cols)
    row = 0
    col = 0
    for i in str:
        #print(i)
        if i == '\n':
            row += 1
            col = 0
        else:
            num = int(i)
            env[row][col] = i
            col += 1

    return env

def setup_screen():
    pg.init()
    screen = pg.display.set_mode([width, height])
    screen.fill(white)
    pg.display.update()
    return screen

def draw_env(env, screen):
    rows = env.shape[0]
    cols = env.shape[1]
    girth = set_girth(env.shape)
    grid_width = int(width/cols)
    grid_height = int(height/rows)
    x = 0
    y = 0

    for i in range(0, cols):
        for j in range (0, rows):
            if env[i][j] == 0:
                pg.draw.rect(screen, black,
                (x, y, grid_width, grid_height)
                , girth)
            else:
                pg.draw.rect(screen, black,
                (x, y, grid_width, grid_height)
                )
            x += grid_width
        x = 0
        y += grid_height
    return screen

def handle_quit():
    while True:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == 27:
                    pg.quit()
                    exit()

def view_env(env):
    print(env)
    screen = setup_screen()
    screen = draw_env(env, screen)
    pg.display.update()
    handle_quit()

def draw_rect(point, color, grid_info, screen):
    grid_width, grid_height = grid_info
    x, y = point
    x *= grid_width
    y *= grid_height
    pg.draw.rect(screen, color,
    (x, y, grid_width, grid_height)
    )
    pg.display.update()
    return screen

def draw_path(path, grid_info, screen, color):
    for foot_print in path:
        point, bool = foot_print
        if bool:
            screen = draw_rect(point, color, grid_info, screen)
        else:
            screen = draw_rect(point, grey, grid_info, screen)
    return screen

def view_path(path, env):

    show_shortest = False
    rows = env.shape[0]
    cols = env.shape[1]

    grid_width = int(width/cols)
    grid_height = int(height/rows)
    grid_info = grid_width, grid_height

    screen = setup_screen()
    screen = draw_env(env, screen)
    pg.display.update()
    start = path[0]
    goal = path[len(path)-1]
    best_path = False

    optimal_path = optimizePath(path)

    foot_print = 0
    pause = True
    show_path = False
    while foot_print < len(path):
        # redraw screen
        screen.fill(white)
        screen = draw_env(env, screen)

        if show_path == True:
            draw_path(path, grid_info, screen, blue)
        if best_path == True:

            draw_path(optimal_path, grid_info, screen, yellow)

        screen = draw_rect(start, green, grid_info, screen)
        screen = draw_rect(goal, blue, grid_info, screen)
        # draw current part green
        x, y = path[foot_print]
        x *= grid_width
        y *= grid_height
        pg.draw.ellipse(screen, red,
        (x, y, grid_width, grid_height)
        )

        pg.display.update()
        pause = True
        while pause == True:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == 27:
                        pg.quit()
                        exit()
                    # p is 112, 80
                    elif event.key == 111 or event.key == 79:
                        if best_path == True:
                            best_path = False
                        else:
                            best_path = True
                        pause = False
                    elif event.key == 112 or event.key == 80:
                        if show_path == True:
                            show_path = False
                        else:
                            show_path = True
                        pause = False
                    elif event.key == 275:
                        if foot_print < len(path):
                            foot_print += 1
                            pause = False
                            break
                    elif event.key == 276:
                        if foot_print > 0:
                            foot_print -= 1
                            pause = False
                    break

    handle_quit()

def get_env(file_name):
    file = open(file_name, 'r')
    str = file.read()
    file = open(file_name, 'r')
    rows = 0
    cols = 0
    for line in file:
        cols = len(line)-1
        rows += 1
    file.close()
    dim = rows, cols

    env = make_env(str, dim)

    return env

def view_all_path(start, goal, env):
    '''
        f for forward A* path
        r steps through all forward A* paths created
        g for optimized forward A* path

        b for backward A* path
        v steps through all backward A* paths created
        n for optimized backward A* path

        a for adaptive A* path
        q steps through all adaptive A* paths
        s for optimized A* path
    '''
    goal = env.shape[0]-1, env.shape[1]-1

    print('generating forward A* path')
    forward_path, cells_expanded = fa.repeated_astar((0,0), goal, env, env.shape, 1)
    print('generating optimized forward A* path')
    forward_path_opti = optimizePath(remove_bool(forward_path[0]))
    forward_path_opti = add_bool(forward_path_opti)

    print('generating backward A* path')
    backward_path, cells_expanded = fa.repeated_astar_backwards((0,0), goal, env, env.shape, 1)
    print('generating optimized backward A* path')
    backward_path_opti = optimizePath(remove_bool(backward_path[0]))
    backward_path_opti = add_bool(backward_path_opti)

    print('generating adaptive A* path')
    adaptive_path, cells_expanded = aa.repeated_astar((0,0), goal, env, env.shape, 1)
    print('generating optimized adaptive A* path', '\n')
    adaptive_path_opti = optimizePath(remove_bool(adaptive_path[0]))
    adaptive_path_opti = add_bool(adaptive_path_opti)

    print('forward A* length', len(forward_path[0]))
    print('optimized forward A* length', len(forward_path_opti), '\n')

    print('backward A* length', len(backward_path[0]))
    print('optimized backward A* length', len(backward_path_opti), '\n')

    print('adaptive A* length', len(adaptive_path[0]))
    print('optimized adaptive A* length', len(adaptive_path_opti), '\n')

    show_forward = False
    forward_i = 0
    show_foward_opti = False

    show_backward = False
    backward_i = 0
    show_backward_opti = False

    show_adaptive = False
    adaptive_i = 0
    show_adaptive_opti = False

    capslock = False

    rows = env.shape[0]
    cols = env.shape[1]

    grid_width = int(width/cols)
    grid_height = int(height/rows)
    grid_info = grid_width, grid_height

    screen = setup_screen()
    screen = draw_env(env, screen)

    pg.display.update()

    run = True
    pause = True
    while run:
        pause = True
        screen.fill(white)
        screen = draw_env(env, screen)
        if show_forward:
            draw_path(forward_path[forward_i], grid_info, screen, dark_red)
        if show_foward_opti:
            draw_path(forward_path_opti, grid_info, screen, red)

        if show_backward:
            draw_path(backward_path[backward_i], grid_info, screen, dark_green)
        if show_backward_opti:
            draw_path(backward_path_opti, grid_info, screen, green)

        if show_adaptive:
            draw_path(adaptive_path[adaptive_i], grid_info, screen, dark_blue)
        if show_adaptive_opti:
            draw_path(adaptive_path_opti, grid_info, screen, blue)

        # show start and finish
        screen = draw_rect(start, yellow, grid_info, screen)
        screen = draw_rect(goal, orange, grid_info, screen)
        while pause:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    # f=102
                    if event.key == 102:
                        show_forward = not show_forward
                    # r=114
                    elif event.key == 114:
                        forward_i += 1
                        if forward_i > len(forward_path)-1:
                            forward_i = 0
                    # g=103
                    elif event.key == 103:
                        show_foward_opti = not show_foward_opti
                    # b=98
                    elif event.key == 98:
                        show_backward = not show_backward
                    # v=118
                    elif event.key == 118:
                        backward_i += 1
                        if backward_i > len(backward_path)-1:
                            backward_i = 0
                    # n=110
                    elif event.key == 110:
                        show_backward_opti = not show_backward_opti
                    # a=97
                    elif event.key == 97:
                        show_adaptive = not show_adaptive
                    # q = 113
                    elif event.key == 113:
                        adaptive_i += 1
                        if adaptive_i > len(adaptive_path)-1:
                            adaptive_i = 0
                    # s=115
                    elif event.key == 115:
                        show_adaptive_opti = not show_adaptive_opti
                    # p=114
                    elif event.key == 112:
                        forward_i = 0
                        backward_i = 0
                        adaptive_i = 0
                    elif event.key == 27:
                        pg.quit()
                        exit()
                    pause = False

            pg.display.update()
