import heapq

def dijkstra(G, source, destination, traffic_factor=1.0):

    pq = [(0, source)]
    distances = {node: float('inf') for node in G.nodes}
    distances[source] = 0

    previous = {node: None for node in G.nodes}

    while pq:
        current_distance, current_node = heapq.heappop(pq)

        if current_node == destination:
            break

        if current_distance > distances[current_node]:
            continue

        for neighbor in G.neighbors(current_node):

            edge_data = G.get_edge_data(current_node, neighbor)

            if not edge_data:
                continue

        
            min_length = min(
                data.get("length", 1) for data in edge_data.values()
            )

            weight = min_length * traffic_factor

            new_distance = current_distance + weight

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current_node
                heapq.heappush(pq, (new_distance, neighbor))

    
    path = []
    node = destination

    if distances[destination] == float('inf'):
        return [], float('inf')

    while node is not None:
        path.append(node)
        node = previous[node]

    path.reverse()

    return path, distances[destination]