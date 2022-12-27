import math
import heapq

class Node:
    cost = None
    h = None
    node = None
    parent = None

    def f(self):
        return self.cost + self.h

    def __lt__(self, other):
        return self.f() <= other.f()

def extend_node(node, cost, h, parent=None):
    n = Node()
    n.node = node
    n.cost = cost
    n.h = h
    n.parent = parent
    return n

class PriorityQueue:
    # with a set

    def __init__(self):
        self.elements = []
        self.set = set([])

    def __str__(self):
        return str(self.elements)

    # for checking if the queue is empty
    def isEmpty(self):
        return len(self.set) == 0

    # for inserting an element in the queue
    def push(self, element):
        heapq.heappush(self.elements, element)
        self.set.add(element.node)

    # for popping an element based on Priority
    def pop(self):
        x = heapq.heappop(self.elements)
        self.set.remove(x.node)
        return x

    def size(self):
        return len(self.set)

    def contains(self, x):
        return x in self.set

    def enforce_invariant(self):
        heapq.heapify(self.elements)

def find_path(get_neighbours, start, end, heuristic=lambda x: math.inf):

    extended_nodes = {}
    extended_start = extend_node(start, 0, heuristic(start))
    extended_nodes[start] = extended_start

    #l_open = [extended_start]
    #set_open = set([start])

    q_open = PriorityQueue()

    #q_open = hq.heapify([])
    #set_open = set([])

    def add_to_queue(x):
        # global q_open, set_open
        set_open.add(x.node)
        hq.heappush(q_open, (x.f(), x))

    def get_from_queue():
        #global q_open, set_open
        x = hq.heappop(q_open)
        set_open.remove(x.node)
        return x[1]

    q_open.push(extended_start)
    #add_to_queue(extended_start)

    set_closed = set([])

    x = None
    while not q_open.isEmpty():
    #while len(l_open) > 0:
    #while not q_open.empty():
        # Take lowest f
        x = q_open.pop()
        # x = q_open.get()

        #m = get_lowest_f(l_open)
        #x = l_open[m]
        #l_open = l_open[:m] + l_open[m+1:]
        #set_open.remove(x.node)

        # print("ALL GOOD")
        
        if x.node == end:
            # Could be extended to a predicate
            print("FINISHED!", x)
            print("Explored...", q_open.size(), len(set_closed))
            return x
        successors = get_neighbours(x.node)
        # print("Successors", successors)
        for nei in successors:
            # 1 is the weight of the edge
            new_cost = x.cost + 1
            if q_open.contains(nei):
                #in set_open:
                # Need something better...
                ext_nei = extended_nodes[nei]
                if ext_nei.cost > new_cost:
                    ext_nei.cost = new_cost
                    ext_nei.parent = x
                    # We have changed a priority
                    # So we need to sort again the queue
                    q_open.enforce_invariant()

            elif nei in set_closed:
                ext_nei = extended_nodes[nei]
                if ext_nei.cost > new_cost:
                    # it costs less to go through x
                    ext_nei.cost = new_cost
                    ext_nei.parent = x
                    
                    # We move the element from the closed list to the open list
                    set_closed.remove(nei)
                    q_open.push(ext_nei)
            else:
                # We create the node, and put it into the open list
                ext_nei = extend_node(nei, new_cost, heuristic(nei), x)
                extended_nodes[nei] = ext_nei
                q_open.push(ext_nei)

        set_closed.add(x.node)
    return (x, q_open.set, set_closed)
