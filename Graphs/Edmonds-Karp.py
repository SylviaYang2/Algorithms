import networkx as nx
import queue

# Part 1: Augmenting Path
# First, you will implement the BFS portion of Edmonds–Karp algorithm.
# Given a graph and s and t vertices, find a augmenting path (a list of vertices
# from s to t including s and t) with BFS. If there's no path, return None.


def bfs_augmenting_path(g: nx.DiGraph, s: int, t: int) -> typing.Union[typing.List[int], None]:
    # Your code here
    n = len(g)
    q = queue.Queue()
    q.put(s)
    path = {s: [s]}

    if s == t:
        return path[s]
    while q.qsize() > 0:
        node = q.get()
        for u, v in g.edges(node):
            if g.edges[u, v]["capacity"] - g.edges[u, v]["flow"] > 0 and v not in path:
                path[v] = path[u] + [v]
                if v == t:
                    return path[v]
                q.put(v)
    return None


# Part 2: Augment
# After finding the augmenting path, now, fill in this function for augment:
# given a s-t path, determine the smallest capacity edge and it will be the
# capacity of the augmenting path. Then, augment the path by decreasing available
# capacity (or increasing flow) for u-v and do the opposite for v-u. Finally,
# return the capacity of the flow you augmented.
def augment(g, path):
    # Your code here
    min_flow = g.edges[path[0], path[1]]["capacity"] - \
        g.edges[path[0], path[1]]["flow"]
    for i in range(2, len(path)):
        min_flow = min(min_flow, g.edges[path[i - 1], path[i]]
                       ["capacity"] - g.edges[path[i - 1], path[i]]["flow"])
    for i in range(1, len(path)):
        g.edges[path[i - 1], path[i]]["flow"] += min_flow
        g.edges[path[i], path[i - 1]]["flow"] -= min_flow
    return min_flow

# Part 3: Edmonds-Karp
# Now, implement Edmonds-Karp with the functions made above:
# a. Find an augmenting path in the graph (with bfs_augmenting_path);
# b. Construct the residual graph by augmenting the path based on the original graph
# and augmenting path (with augment);
# c. Do this until no augmenting path can be found.
# Return the capacity and the final residual graph.


def edmonds_karp(gg: nx.DiGraph, s, t) -> typing.Tuple[int, nx.DiGraph]:
    g = nx.algorithms.flow.build_residual_network(gg.copy(), "capacity")
    nx.set_edge_attributes(g, 0, "flow")
    # Your code here
    max_flow = 0
    n = len(g)
    path = bfs_augmenting_path(g, s, t)
    while path != None:
        flow = augment(g, path)
        path = bfs_augmenting_path(g, s, t)
        max_flow += flow
    return (max_flow, g)
