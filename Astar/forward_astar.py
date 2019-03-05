#
#   Authors: Steven Freed, Samuel Jefferson
#

import minHeap as mh

# State for each coordinate
class State:
    def __init__(self, point, g, f):
        self.point = point
        self.g = g
        self.f = f

# finds the shortest path
#
# @param start          starting coordinate
# @param goal           goal coordinate
# @param blocked_dict   blocked coordinates
# @param dim            dimensions of grid
# @return total_path    list of coordinates making up the shortest path
def astar(start, goal, blocked_dict, dim, tie_break):

    # evaluated nodes
    closed_dict = {}

    # map of points associated with the point it came from
    came_from = {}

    # map of points and thier costs
    g_score = {
        start: 0
    }

    # nodes waiting to be evaluated
    open_list = mh.MinHeap(tie_break)
    open_list.insert(State(start, 0, heuristic(start, goal)), g_score)

    # number of nodes expanded
    cells_expanded = 0

    while len(open_list.heap) > 0:

        current = open_list.heap[0]

        # if the goal is found, get shortest path
        if current.point == goal:
            #print(reconstruct_path(came_from, current.point))
            return reconstruct_path(came_from, current.point), cells_expanded

        if current in open_list.heap:
            open_list.pop()

        closed_dict[current.point] = True

        # iterates through all neighboring nodes
        neighborhood = neighborsOf(current.point, blocked_dict, dim)

        for neighbor in neighborhood:

            if closed_dict.get(neighbor.point, False) == True:
                continue

            cells_expanded += 1

            # The distance from current node to a neighbor plus the past cost from start to current node
            new_g_score = g_score[current.point] + 1

            came_from[neighbor.point] = current.point
            g_score[neighbor.point] = new_g_score
            neighbor.g = g_score[neighbor.point]
            neighbor.f = g_score[neighbor.point] + heuristic(neighbor.point, goal)

            if neighbor not in open_list.heap:
                open_list.insert(neighbor, g_score)
    # TODO here
    return -1


# finds the shortest path by decoding the came_from dictionary
# and prints the shortest path
#
# @param came_from  the dictionary of where nodes came from to find the path
# @param current    the current node
# @return           the shortest path total
def reconstruct_path(came_from, current):
    total_path = [current]

    while current in came_from.keys():
        current = came_from[current]
        total_path = [current] + total_path

    return total_path

# calculates Manhattan distance heuristic
#
# @param coordinates    current node
# @param goal           goal node
# @return               the Manhattan distance
def heuristic(coordinates, goal):
    x1, y1 = coordinates
    x2, y2 = goal
    return abs(x1 - x2) + abs(y1 - y2)

# calculates the cost to go to each neighbor and if they are blocked
#
# @param state          current state
# @param blocked_dict   so we can tell if they are blocked
# @param dim            so we know if the current state is out of bounds
def neighborsOf(state, blocked_dict, dim):
    x_max, y_max = dim
    neighbors = []
    top = State((state[0]-1, state[1]), 0, 1000)
    bottom = State((state[0]+1, state[1]), 0, 1000)
    left = State((state[0], state[1]-1), 0, 1000)
    right = State((state[0], state[1]+1), 0, 1000)
    # adds neighbor to list of neighbors if is > -1 and isn't blocked
    if top.point[0] > -1 and top.point[1] > -1 and blocked_dict.get(top.point, False) == False:
        if top.point[0] < x_max and top.point[1] < y_max:
            neighbors.append(top)

    if bottom.point[0] > -1 and bottom.point[1] > -1 and blocked_dict.get(bottom.point, False) == False:
        if bottom.point[0] < x_max and bottom.point[1] < y_max:
            neighbors.append(bottom)

    if left.point[0] > -1 and left.point[1] > -1 and blocked_dict.get(left.point, False) == False:
        if left.point[0] < x_max and left.point[1] < y_max:
            neighbors.append(left)

    if right.point[0] > -1 and right.point[1] > -1 and blocked_dict.get(right.point, False) == False:
        if right.point[0] < x_max and right.point[1] < y_max:
            neighbors.append(right)

    return neighbors

def get_point(point, env):
    x, y = point
    return env[y][x]

# runs A* on environment
# just A*, not repeated A* or adaptive A*
# used by sidewinder to make sure that the created maze has a path
def astar_env(start, goal, env, dim):
    # if the starting point is blocked
    if get_point(start, env) == 1:
        print('starting point is blocked')
        return False
    current = start
    blocked_dict ={}
    final_path = []
    # fill blocked dict
    rows, cols = dim
    for i in range(0, rows):
        for j in range(0, cols):
            point = i, j
            if get_point(point, env) == 1:
                blocked_dict[point] = True

    path = astar(current, goal, blocked_dict, dim, 1)
    return path

# repeated astar to calculate blocked points and run astar many times after hitting blocks
#
# @param start  starting node coordinates
# @param goal   ending node coordinates
# @param env    GUI environment
# @param dim    dimensions of grid
# @return       shortest path and cells expanded
def repeated_astar(start, goal, env, dim, tie_breaker):
    # if the starting point is blocked
    if get_point(start, env) == 1:
        print('starting point is blocked')
        return False
    current = start
    blocked_dict ={}
    tie_break = tie_breaker
    final_path = []
    all_paths = []
    i = 1
    cells_expanded = 0
    while current != goal:
        i += 1
        # TODO here
        #path, temp_expanded = astar(current, goal, blocked_dict, dim, tie_break)
        temp = astar(current, goal, blocked_dict, dim, tie_break)
        if temp == -1:
            return all_paths, cells_expanded

        path, temp_expanded = temp

        cells_expanded += temp_expanded
        temp_path = []
        for point in path:
            if get_point(point, env) == 1:
                temp_path.append((point, False))
                blocked_dict[point] = True
                break
            else:
                temp_path.append((point, True))
                current = point
                if len(final_path) > 0:
                    if current != final_path[len(final_path)-1]:
                        final_path.append((current, True))
                else:
                    final_path.append((current, True))
        all_paths.append(temp_path)

    all_paths.insert(0, final_path)

    return all_paths, cells_expanded

# repeated_astar_backwards
def repeated_astar_backwards(start, goal, env, dim, tie_breaker):
    return repeated_astar(goal, start, env, dim, tie_breaker)
