# A* Algorithm Variations
This project contains A* variations such as; Repeated Forwards A*, Repeated Backwards A*, and Adaptive A*. The UI was written using pygame. The priority queue for the algorithms is implemented using a minheap that can break f (f = h + g or heuristic plus cost) value ties based on higher or lower g values.

## Instructions
1. pick a maze from the maze folder (sidewinderN.txt, where N is a number from 0-9) and run the program using...
```
$ python presentation.py mazes/sidewinderN.txt
```

2. Press a key to see results...
```
p - resets all paths

f - for forward A* path
r - steps through all forward A* paths created
g - for optimized forward A* path

b - for backward A* path
v - steps through all backward A* paths created
n - for optimized backward A* path

a - for adaptive A* path
q - steps through all adaptive A* paths
s - for optimized A* path
```

## Screen Shots
Forward A*<br>
Red - all blocked encounters<br>
Light Red - optimal path

Backward A*<br>
Green - all blocked encounters<br>
Light Green - optimal path

Adaptive A*<br>
Blue - all blocked encounters<br>
Light Blue - optimal path

| ![Alt text](astar.png?raw=true) |
|:--:|
| *Pygame UI Astar* |
