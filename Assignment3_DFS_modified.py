from collections import defaultdict
from pprint import pprint
import re
import timeit

# Define class Graph:
class Graph:
    def __init__(self, gr=[]):
        self.gr = defaultdict(list)

    def add_edge(self, u, v):
        self.gr[u].append(v)

    def list_all_vertices(self):
        vertices = []
        for u in self.gr:
            vertices.append(u)

        for u in self.gr:
            for v in self.gr[u]:
                vertices.append(v)
        self.list_vertices = list(set(vertices))

        return list(self.list_vertices)


def DFS_visit(u, adj_list, time, graph, edges, order):
    """
    This function recursively walks along the adjacency lists and collect information about 
    the types of each edge.
    Inputs:
    u - vertex object.
    adj_list - adjacency list for the vertex u.
    time - current time of the function call.
    graph - graph object.
    edges - dictionary of edges and their type.
    order - order of when each vertex was discovered.
    """
    # Color u vertex as 'discovered':
    u.color = 'gray'
    # Increment 'time' by 1:
    time = time + 1
    # Assign time to u vertex:
    u.d = time
    
    # Add the vertex to the order list:
    order.append(u.index)
    # Check if the adjecency list of u vertex is not empty:
    if len(adj_list) != 0:
        for v in adj_list:
            # Check if the next vertex is 'white' and if so, make u its predecessor, update edges dictionary,
            # recursively call DSF_visit on this vertex.
            if v.color == 'white':
                v.predecessor = u
                edges['tree'].append((u.index, v.index))
                finish_time = DFS_visit(v, graph.gr[v], time, graph, edges, order)
                time = finish_time
            # Check if the next vertex is 'gray' and if so, update edges dictionary:
            elif v.color == 'gray':
                edges['back'].append((u.index, v.index))
            # Check if the next vertex is 'black' and it is a descendant of u, then update edges dictionary.
            elif v.color == 'black' and v.d > u.d:
                edges['forward'].append((u.index, v.index))
            # Check if this is another case, then update edges dictionary.
            else:
                edges['cross'].append((u.index, v.index))
    # Finalize u vertex:
    u.color = 'black'
    # Increment 'time' by 1:
    time = time + 1
    u.f = time

    return time


def DFS_edge_names(graph):
    """
    This function takes Graph object as input and returns dictionary edges and the order of how the traverse of the graph
    happened.
    """
    # Initialize order list and edges dictionary:
    order = []
    edges = {'tree' : [], 'back' : [], 'forward' : [], 'cross' : []}
    
    # Get all vertices of the graph as a list:
    vertices = graph.list_all_vertices()
    
    # Set time = 0
    time = 0
    
    # Start traverse of the graph from picking a random starting point 
    # (random happens when we call method 'list_all_vertices')
    for u in vertices:
        if u.color == 'white': # Check if the next vertex is undiscovered yet
            # Call DFS_visit on adjacency list for the vertex u.
            # Return finish time for the given starting point:
            finish_time = DFS_visit(u, graph.gr[u], time, graph, edges, order) 
            # Update current time variable:
            time = finish_time
    # Print vetrices' parameters in the order they were discovered:
    for i in order:
        for u in vertices:
            if u.index == i:
                print(f'vertex = {u.index}, v.d = {u.d}, v.f = {u.f}')
                
    # Print the order of the vertices they were discovered:
    print('\n', 30*'=')
    print('Having traverse order:')
    print(*order)
    print('Following edges were discovered:')
    # Print all edges of the graph and their type:
    pprint(edges)

    return edges, order

# Define a node object with initializing parameters:
class Node:
    def __init__(self, index):
        self.index = index
        self.color = 'white'
        self.predecessor = None
        self.d = 0
        self.f = 0

if __name__ == '__main__':
    """
    The input txt file must be looking like this:
    (1, 2)
    (1, 3)
    (1, 4)
    (2, 3)
    (2, 4)
    ...
    I.e. each row must represent an existing direction in the graph.
    
    To generate random size input you may use small subprogram Assignment3_generate_input.py, which is located in the same folder.
    """
    file_vertx = "./Ass3_input.txt"
#     file_vertx = "./output.txt"

    # Initialize empty graph g:
    g = Graph()
    
    vert = []
    # This part read from the input file, line by line, and build a graph g:
    with open(file_vertx) as fp:
        for line in fp:
            a, b = re.findall(r'\d+', line)
            
            if a in vert and b in vert:
                g.add_edge(locals()['v' + str(a)], locals()['v' + str(b)])
            elif (a not in vert) and (b not in vert):
                vert.append(a)
                vert.append(b)
                locals()['v' + str(a)] = Node(a)
                locals()['v' + str(b)] = Node(b)
                g.add_edge(locals()['v' + str(a)], locals()['v' + str(b)])
            
            if (a in vert) and (b not in vert):
                vert.append(b)
                locals()['v' + str(b)] = Node(b)
                g.add_edge(locals()['v' + str(a)], locals()['v' + str(b)])
            elif (a not in vert) and (b in vert):
                vert.append(a)
                locals()['v' + str(a)] = Node(a)
                g.add_edge(locals()['v' + str(a)], locals()['v' + str(b)])
    
    # Main call:
    order, edges = DFS_edge_names(g)