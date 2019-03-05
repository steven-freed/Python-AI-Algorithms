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
# @param new_h_score    the informed h scores based on the knoledge of the blocked_dict
# @return total_path    list of coordinates making up the shortest path
def adapt_astar(start, goal, blocked_dict, new_h_score, dim, tie_break):

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
    new_node = State(start, 0, heuristic(start, goal))
    open_list.insert(new_node, g_score)

    # number of nodes expanded
    cells_expanded = 0

    while len(open_list.heap) > 0:

        current = open_list.heap[0]

        # if the goal is found, get shortest path
        if current.point == goal:
            return reconstruct_path(came_from, current.point, g_score, blocked_dict), cells_expanded

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

            # if an informed heuristic exists use that instead of the old heuristic
            if (neighbor.point in new_h_score):
                neighbor.f = g_score[neighbor.point] + new_h_score[neighbor.point]
            else:
                neighbor.f = g_score[neighbor.point] + heuristic(neighbor.point, goal)

            if neighbor not in open_list.heap:
                open_list.insert(neighbor, g_score)
    # TODO Here
    return -1


# Adjusts heuristics for all values in path but not in blocked list
#   NOTE: new_h_score = (cost to get to goal taking 'path') - (states g value for a* iteration that just ran)
#
# @param cost       cost of the shortest path for the previous astar iteration
# @param path       the shortest path for the previous astar iteration
# @param g_score    dictionary of the costs for all encountered nodes
# @param blocked    all blocked nodes
# @return           a dictionary of the informed heuristics for all encountered nodes
def adjust_heuristics(cost, path, g_score, blocked):
    new_h_score = {}

    for s in path:
        if s not in blocked.keys():
            new_h_score[s] = cost - g_score[s]

    return new_h_score

# finds the shortest path by decoding the came_from dictionary
# and prints the shortest path
#
# @param came_from  the dictionary of where nodes came from to find the path
# @param current    the current node
# @param g_scores   the costs for each node
# @param blocked    the blocked nodes
# @return           the length of the path, the shortest path total, the g_scores for all encountered nodes
def reconstruct_path(came_from, current, g_scores, blocked):
    total_path = [current]

    while current in came_from.keys():
        current = came_from[current]
        total_path = [current] + total_path

    count = len(total_path)-1

    return count, total_path, g_scores

# calculates Manhattan distance heuristic
#
# @param coordinates    current node
# @param goal           goal node
# @return               the Manhattan distance
def heuristic(neighbor, goal):
    x1, y1 = neighbor
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

# creates GUI
def repeated_astar(start, goal, env, dim, tie_breaker):
    # if the starting point is blocked
    if get_point(start, env) == 1:
        print('starting point is blocked')
        return False
    current = start
    blocked_dict = {}
    new_h_score = {} # map of points to informed h values
    tie_break = tie_breaker # breaks ties with high or low g value
    final_path = []
    all_paths = []
    i = 1
    cells_expanded = 0
    while current != goal:
        i += 1
        #count, path, g_scores, temp_expanded = adapt_astar(current, goal, blocked_dict, new_h_score, dim, tie_break)
        #temp, temp_expanded = adapt_astar(current, goal, blocked_dict, new_h_score, dim, tie_break)
        temp2 = adapt_astar(current, goal, blocked_dict, new_h_score, dim, tie_break)
        if temp2 == -1:
            # TODO here
            return all_paths, cells_expanded
        temp, temp_expanded = temp2
        count, path, g_scores = temp
        cells_expanded += temp_expanded
        temp_path = []
        for point in path:
            if get_point(point, env) == 1:
                temp_path.append((point, False))
                blocked_dict[point] = True

                # Once blocked_dict is populated 'adjust_heuristics' takes args returned from adapt_astar
                # and calculates the new h values for all non-blocked states in 'path'
                # Then adds those updates h values to the 'new_h_score' dict
                new_h_score.update(adjust_heuristics(count, path, g_scores, blocked_dict))
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

    adjust_heuristics(count, path, g_scores, blocked_dict)
    return all_paths, cells_expanded
