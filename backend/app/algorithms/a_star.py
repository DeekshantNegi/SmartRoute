import heapq
import math

# 🧠 Heuristic function (Haversine distance)
def heuristic(G, node1, node2):
    x1, y1 = G.nodes[node1]["x"], G.nodes[node1]["y"]
    x2, y2 = G.nodes[node2]["x"], G.nodes[node2]["y"]

    # simple euclidean (fast)
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)


def astar(G, source, destination, traffic_factor=1.0):

    pq = [(0, source)]  # (f_score, node)

    g_cost = {node: float('inf') for node in G.nodes}
    g_cost[source] = 0

    f_cost = {node: float('inf') for node in G.nodes}
    f_cost[source] = heuristic(G, source, destination)

    previous = {node: None for node in G.nodes}

    while pq:
        current_f, current_node = heapq.heappop(pq)

        if current_node == destination:
            break

        for neighbor in G.neighbors(current_node):

            edge_data = G.get_edge_data(current_node, neighbor)
            if not edge_data:
                continue

            # ✅ handle MultiDiGraph (same as your code)
            min_length = min(
                data.get("length", 1) for data in edge_data.values()
            )

            weight = min_length * traffic_factor

            tentative_g = g_cost[current_node] + weight

            if tentative_g < g_cost[neighbor]:
                previous[neighbor] = current_node
                g_cost[neighbor] = tentative_g

                f_cost[neighbor] = tentative_g + heuristic(G, neighbor, destination)

                heapq.heappush(pq, (f_cost[neighbor], neighbor))

    # 🔁 reconstruct path
    path = []
    node = destination

    if g_cost[destination] == float('inf'):
        return [], float('inf')

    while node is not None:
        path.append(node)
        node = previous[node]

    path.reverse()

    return path, g_cost[destination]