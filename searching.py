goal = None # initializes goal
graph = [] # initializes graph

'''
    State for Path Searching:
        contains meta data about a location or states; id, coordinates, heuristic, and edges
        id - a string or number to uniquely identify a state
        coordinates - to mark a state in a coordinate plane
        heuristic - staight line distance from state to goal state
        edges - a dictionary with keys as state ids and values as the cost to go to that state
'''
class State:
    # inits a Node with coordinates and a heuristic given a goal
    def __init__(self, id, coordinates, edges):
            self.id = id
            self.coordinates = coordinates
            if goal != None:
                self.heuristic = self.getHeuristic(goal)
                self.edges = self.getCosts(edges)
            else:
                self.heuristic = 0
                self.edges = {}

    # Gets the cost to go to the next node
    def getCosts(self, edges):
        costs = {}

        for edge in edges:
            costs[edge] = self.getHeuristic(edge)

        return costs

    # calculates the heuristic based on the init parameters
    def getHeuristic(self, goal):
        x1 = self.coordinates[0]
        y1 = self.coordinates[1]
        x2 = goal.coordinates[0]
        y2 = goal.coordinates[1]
        return abs(x1 - x2) + abs(y1 - y2)

    # prints formatted Node data
    def __str__(self):
        return "{\nid: %s\ncoordinates: %s\nheuristic: %s\nedges: %s\n}" % (self.id, self.coordinates, str(self.heuristic), str(self.edges))

'''
    A* Search Algorithm:
        Designed to work with Strings and Numbers
'''
def astar(list):

    start = list[0] # starting state

    frontier = [(start.heuristic, start)] # open list of states (Priority Queue)
    came_from = {} # each states previous state
    cost_so_far = {} # cost of current and all previous states
    came_from[start.id] = None
    cost_so_far[start.id] = 0

    # traverses the frontier
    while len(frontier) > 0:
        curr = frontier.pop()[1]
        neighbors = [*curr.edges.keys()]

        # if current state is the goal state
        if curr.id == goal.id:
            break

        # traverses all neighbors for the current state
        for next in range(len(neighbors)):
            new_cost = cost_so_far[curr.id] + curr.edges[neighbors[next]] # cost of current state and previous states
            # if neighbors cost hasn't been considered OR
            # the total cost is less than the cost of the whole current path
            if neighbors[next] not in cost_so_far or new_cost < cost_so_far[neighbors[next]]:
                cost_so_far[neighbors[next].id] = new_cost
                fn = new_cost + neighbors[next].heuristic # total costs plus heuristic
                frontier.append((fn, neighbors[next]))
                frontier.sort(key=lambda tup: tup[0], reverse=True)
                came_from[neighbors[next].id] = curr.id

    # gets shortest path from a dictionary
    # dictionary contains all state ids corresponding to the state id that each came from
    c = goal.id
    s = start.id
    shortest = []
    index = 0
    while c != s:
        shortest = [c] + shortest
        c = came_from[c]
        index += 1
    shortest = [s] + shortest

    return shortest


# States for a graph
goal = State(5, (5, 5), [])
n3 = State(3, (2, 5), [goal])
n4 = State(4, (5, 2), [goal])
n2 = State(2, (1, 3), [n4, goal, n3])
n1 = State(1, (3, 1), [n4])
n0 = State(0, (0, 0), [n1, n2])

# append nodes to graph
graph.append(n0)
graph.append(n1)
graph.append(n2)
graph.append(n3)
graph.append(n4)
graph.append(goal)

print(astar(graph))

'''
def print_path(dim):
    dimensions = dim+1
    y = 0
    x = 0

    for x in range(dimensions):
        for y in range(dimensions):
            print('.', end=' ')
        print()
'''
