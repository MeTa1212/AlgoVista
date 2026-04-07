import random


# ─────────────────────────────────────────────────────────────────
#  SAFETY CHECK
# ─────────────────────────────────────────────────────────────────

def is_safe(v, graph, path, pos):
    if graph[path[pos - 1]][v] == 0:
        return False
    if v in path:
        return False
    return True


# ─────────────────────────────────────────────────────────────────
#  VISUALISATION GENERATOR
#
#  Yields: (path, state, message)
#    state = "normal"    → amber  – currently exploring this path
#    state = "backtrack" → red    – dead-end; about to backtrack
#    state = "found"     → green  – Hamiltonian cycle confirmed
# ─────────────────────────────────────────────────────────────────

def hamiltonian_cycle_visual(graph):
    n     = len(graph)
    path  = [0]
    steps = []

    # Step 0 — only starting node, no edges yet
    steps.append((path.copy(), "normal", "Starting from node 0"))

    def solve(pos):
        if pos == n:
            if graph[path[pos - 1]][path[0]] == 1:
                # Full cycle found — yield green
                steps.append((path.copy() + [path[0]], "found",
                               "✅ Hamiltonian Cycle Found!"))
                return True
            else:
                # All nodes visited but no closing edge — dead-end (red)
                steps.append((path.copy(), "backtrack",
                               "All nodes visited — no return edge to start"))
                return False

        for v in range(1, n):
            if is_safe(v, graph, path, pos):
                path.append(v)
                # Exploring — yellow
                steps.append((path.copy(), "normal", f"Trying node {v}"))
                if solve(pos + 1):
                    return True
                # Dead-end reached deeper — show red BEFORE popping
                steps.append((path.copy(), "backtrack",
                               f"Dead end — backtracking from node {v}"))
                path.pop()
                # After backtrack — yellow again (shorter path)
                steps.append((path.copy(), "normal",
                               f"Backtracked to path of length {len(path)}"))

        return False

    found = solve(1)

    if not found:
        steps.append((path.copy(), "backtrack",
                      "❌ No Hamiltonian Cycle exists in this graph"))

    for step in steps:
        yield step


# ─────────────────────────────────────────────────────────────────
#  GRAPH GENERATORS
# ─────────────────────────────────────────────────────────────────

def generate_graph_with_cycle(n):
    """Guarantee a Hamiltonian cycle by building one explicitly."""
    graph = [[0] * n for _ in range(n)]

    perm = list(range(n))
    random.shuffle(perm)
    for i in range(n):
        u = perm[i]
        v = perm[(i + 1) % n]
        graph[u][v] = 1
        graph[v][u] = 1

    # Add random extra edges
    for _ in range(max(1, n // 2)):
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v:
            graph[u][v] = 1
            graph[v][u] = 1

    return graph


def _has_hamiltonian_cycle(graph):
    """Brute-force check used during generation (n ≤ 8 only)."""
    n    = len(graph)
    path = [0]

    def solve(pos):
        if pos == n:
            return graph[path[-1]][path[0]] == 1
        for v in range(1, n):
            if graph[path[-1]][v] == 1 and v not in path:
                path.append(v)
                if solve(pos + 1):
                    return True
                path.pop()
        return False

    return solve(1)


def generate_graph_without_cycle(n):
    """
    Build a graph guaranteed NOT to contain a Hamiltonian cycle.
    Verified with brute-force; retries up to 200 times.
    """
    for _ in range(200):
        graph = [[0] * n for _ in range(n)]

        # Backbone: simple path 0−1−2−…−(n-1), no closing edge
        for i in range(n - 1):
            graph[i][i + 1] = 1
            graph[i + 1][i] = 1
        graph[0][n - 1] = 0
        graph[n - 1][0] = 0

        # A few interior short-range extras
        for _ in range(max(1, n // 3)):
            u = random.randint(1, n - 3)
            v = random.randint(u + 2, n - 2)
            graph[u][v] = 1
            graph[v][u] = 1

        if not _has_hamiltonian_cycle(graph):
            return graph

    # Fallback: pure path (provably no Hamiltonian cycle)
    graph = [[0] * n for _ in range(n)]
    for i in range(n - 1):
        graph[i][i + 1] = 1
        graph[i + 1][i] = 1
    return graph