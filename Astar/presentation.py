#
#   Authors: Steven Freed, Samuel Jefferson, Anthony Pensak
#

'''
    run with "python presentation.py small_mazes/smallwinder0.txt"
    you can replace the last argument with a different maze
    such as "python presentation.py mazes/sidewinder0.txt"

    p resets all paths

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

import sidewinder as sw
import forward_astar as fa
import adaptive_astar as aa
import view
import time
import sys

if len(sys.argv) == 1:
    print('Enter gridworld name as command line argument')
elif len(sys.argv) > 2:
    print('Error: too many arguments')


filename = list(sys.argv)[1]
env = view.get_env(filename)

goal = env.shape[0]-1, env.shape[1]-1
print(goal)
view.view_all_path((0,0), goal, env)
