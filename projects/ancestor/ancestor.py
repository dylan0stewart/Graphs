class Stack():
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None

    def size(self):
        return len(self.stack)


class Graph:
    def __init__(self):
        self.vertices = {}

    def add_vertices(self, vertex):
        if vertex not in self.vertices:
            self.vertices[vertex] = set()

    def add_edge(self, v1, v2):
        self.vertices[v1].add(v2)

    def get_neighbors(self, vertex):
        return self.vertices[vertex]



def make_graph(ancestors):
    graph = Graph()
    for parent, child in ancestors:
        graph.add_vertices(parent)
        graph.add_vertices(child)
        graph.add_edge(child, parent)
    return graph

def earliest_ancestor(ancestors, starting_node):
    graph = make_graph(ancestors) # make graph

    s = Stack()
    visited = set()
    s.push([starting_node])
    longest_path = [] # instantiate a longest_path list for later

    while s.size() > 0: # while the stack has items
        path = s.pop() # pull the path out and instantiate
        current_node = path[-1] # get the last item in path for the current node

        if len(path) > len(longest_path): #if current path is longer than current longest, make current the new longest
            longest_path = path

        if current_node not in visited: # if current node isnt already in visited
            visited.add(current_node) # make sure it gets logged as visited
            parents = graph.get_neighbors(current_node) # use get_neghbors to get and assign the parent nodes

            for parent in parents: # for each parent
                new_path = path+[parent] # make a new path for each parent
                s.push(new_path)
    if starting_node == longest_path[-1]:
        return -1
    else:
        return longest_path[-1] # return last item in the longest path
    