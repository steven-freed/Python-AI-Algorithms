#
#   Authors: Samuel Jefferson
#

# adapted from
# http://weblog.jamisbuck.org/2011/2/3/maze-generation-sidewinder-algorithm

import numpy as np
import forward_astar as fa

def go_east(east_percent):
    if np.random.random() < east_percent:
        return True
    else:
        return False

def get_paths_up(left, right, row, env):
    up_chance = 0.4
    up_count = int((right-left)*up_chance)
    if up_count < 1:
        up_count = 1
    #print('uc', up_count)
    i = 0
    while i < up_count:
        path_up = np.random.randint(left, right+1)
        if env[row-1][path_up] == 1:
            env[row-1][path_up] = 0
            i += 1

    return env

def gen_maze(rows, cols, east_percent=1):
    env = np.ones(rows * cols).reshape(rows,cols)

    skip = False
    for i in range (0, rows):
        if i % 2 == 0:
            left = 0
            right = 0
            for j in range(0, cols):
                # the first row is always empty
                if skip:
                    skip = False
                    left = j + 1
                elif i == 0:
                    if j < 10:
                        env[i][j] = 0
                    elif np.random.random() < 0.9:
                        env[i][j] = 0
                elif go_east(east_percent) == True:
                    env[i][j] = 0
                    # if the row goes to the end of the end
                    if j == cols-1:
                        right = j
                        path_up = get_paths_up(left, right, i, env)
                else:
                    env[i][j] = 0
                    right = j
                    env = get_paths_up(left, right, i, env)
                    skip = True
                    left = j
    env[rows-1][cols-1] = 0
    return env

def write_maze(name, rows, cols, env_count=1, east_percent=0.85):
    ext = ".txt"

    for i in range(env_count):
        path = None
        while path == None:
            filename = name + str(i) + ext
            print("generating maze", filename)
            env = gen_maze(rows, cols, 0.90)
            # make sure there is a path
            print('checking for path')
            print(rows-1, cols-1)
            path, cells_expanded = fa.astar_env((0,0), (rows-1, cols-1), env, (rows, cols))
            #print('path', path)
            print('path found')
        np.savetxt(filename, env, fmt='%d', delimiter='')
