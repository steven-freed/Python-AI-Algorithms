#
#   Authors: Steven Freed
#

#
#    MinHeap:
#        ::- parent = FLOOR(index/2)
#        ::- left child = (2 * index) + 1
#        ::- right child = (2 * index) + 2
#

class State:
    def __init__(self, point, g, f):
        self.point = point
        self.g = g
        self.f = f

class MinHeap:

    # @param type   negative number to break ties with lower g values,
    #               positive number to break ties with higher g values
    def __init__(self, type=-1):
        self.heap = []
        self.type = type

    # gets parent index of a node
    #
    # @param ofIndex    index of node
    # @return           index of parent to the given node
    def parentIndex(self, ofIndex):
        return int((ofIndex-1)/2)

    # gets left child index of a node
    #
    # @param ofIndex    index of node
    # @return           index of left child to the given node
    def leftIndex(self, ofIndex):
        return int((2*ofIndex)+1)

    # gets right child index of a node
    #
    # @param ofIndex    index of node
    # @return           index of right child to the given node
    def rightIndex(self, ofIndex):
        return int((2*ofIndex)+2)

    # @return   the min of the heap
    def peek(self):
        return self.heap[0]

    # swaps nodes until heap is balanced
    #
    # @param index  index of node in heap
    def heapify(self, index):

        if not(self.heap[self.parentIndex(0)] != None and self.heap[index].f < self.heap[self.parentIndex(0)].f):

            while(self.leftIndex(index) < len(self.heap) and self.rightIndex(index) < len(self.heap)):

                left = self.leftIndex(index)
                right = self.rightIndex(index)

                if self.heap[left].f < self.heap[right].f:
                    self.heap[index], self.heap[left] = self.heap[left], self.heap[index]
                    index = left
                else:
                    self.heap[index], self.heap[right] = self.heap[right], self.heap[index]
                    index = right

    # deletes the min from the heap and rebalances it
    #
    # @return   None if heap is empty, else the node in the heap
    def pop(self):
        if len(self.heap) < 2:
            node = self.heap.pop(0)
            return
        node = self.heap.pop(0)
        last_element = self.heap[-1]
        self.heap.insert(0, last_element)
        self.heap.pop()
        self.heapify(0)

        return node

    # Inserts element into heap
    # @param key       key you want to add to heap
    # @return          True on sucessful insert, False on failure
    def insert(self, key, g_score):

        '''
            Added for breaking f ties so no need to break g ties unless of emergency
        '''
        c = max(g_score.values()) # g value larger than the largest g value of all nodes

        if self.type >= 0:
            # newf = c*f - g break larger g ties
            key.f = ((c + 1 * key.f) - key.g)
        else:
            # newf = c*f + g break smaller g ties
            key.f = ((c + 1 * key.f) + key.g)

        # if heap contains less than 1 node
        if len(self.heap) < 1:
            self.heap.append(key)
            return

        self.heap.append(key)
        index = len(self.heap) - 1

        # if current index has a parent node AND that parent has a greater value than the current node
        while(self.parentIndex(index) > -1 and self.heap[self.parentIndex(index)].f > self.heap[index].f):
            self.heap[self.parentIndex(index)], self.heap[index] = self.heap[index], self.heap[self.parentIndex(index)]
            index = self.parentIndex(index)

    # Overrides str function to print out heap
    def __str__(self):
        stri = ""
        for s in self.heap:
            stri = stri + " point="+ str(s.point) + " f=" + str(s.f) + "\n"

        return stri
