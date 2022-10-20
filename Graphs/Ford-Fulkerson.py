# MAXIMUM FLOW VIA FORD FULKERSON

# input in adj matrix representation
# u[i][j] is capacity of edge (i,j) (0 if edge not present)
def ford_fulkerson(u, s, t):
    n = len(u)
    f = [[0] * n for _ in range(n)]
    max_flow = 0

    def dfs(v, flow, f):
        nonlocal n, u, t, visited
        # Base case
        if v == t:
            return flow

        # Loop through every edge
        for w in range(n):
            if not visited[w]:
                residual = u[v][w] - f[v][w]
                if residual > 0:
                    visited[w] = True
                    # keep the min of the previous bottleneck value and the current edge's residual
                    bottleneck = dfs(w, min(flow, residual), f)
                    # augmenting the edge
                    f[v][w] += bottleneck
                    f[w][v] -= bottleneck
                    return bottleneck
        return 0

    # Do this until no augmenting path can be found
    visited = []
    while True:
        visited = [False] * n
        visited[s] = True
        amt = dfs(s, float('infinity'), f)
        if amt == 0:  # no more augmenting path
            break
        max_flow += amt

    # return max_flow
    for i in range(n):
        for j in range(n):
            f[i][j] = max(f[i][j], 0)
    return max_flow


capacities = [
    [0, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 0],
    [0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0]
]

print(ford_fulkerson(capacities, 0, 5))
