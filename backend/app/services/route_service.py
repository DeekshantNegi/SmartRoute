import osmnx as ox
import networkx as nx
import math

from app.core.cache import get_graph_from_cache, set_graph_in_cache

# 🔥 Fuel cost config
COST_PER_KM = 5


# =========================================================
# 🌍 Convert place → coordinates
# =========================================================
def geocode_place(place: str):
    lat, lon = ox.geocode(place)
    return [lat, lon]


# =========================================================
# 🚀 Load graph (cached)
# =========================================================
def get_graph():
    key = "dehradun_graph"

    cached_graph = get_graph_from_cache(key)
    if cached_graph:
        print("✅ Using cached graph")
        return cached_graph

    print("⬇️ Downloading graph ONLY ONCE...")

    G = ox.graph_from_place(
        "Dehradun, Uttarakhand, India",
        network_type="drive"
    )

    G_simple = nx.DiGraph()

    for u, v, data in G.edges(data=True):
        weight = data.get("length", 1)

        if G_simple.has_edge(u, v):
            if G_simple[u][v]["length"] > weight:
                G_simple[u][v]["length"] = weight
        else:
            G_simple.add_edge(u, v, length=weight)

    for node, data in G.nodes(data=True):
        G_simple.add_node(node, **data)

    G_simple.graph = G.graph

    set_graph_in_cache(key, G_simple)

    return G_simple


# =========================================================
# 📍 Get nearest nodes
# =========================================================
def get_nearest_nodes(G, source_coords, dest_coords):
    orig = ox.distance.nearest_nodes(G, source_coords[1], source_coords[0])
    dest = ox.distance.nearest_nodes(G, dest_coords[1], dest_coords[0])
    return orig, dest


# =========================================================
# 🗺 Convert nodes → coordinates
# =========================================================
def nodes_to_coordinates(G, route):
    return [[G.nodes[node]["x"], G.nodes[node]["y"]] for node in route]


# =========================================================
# ⛽ Fuel cost
# =========================================================
def calculate_fuel_cost(distance_m):
    return round((distance_m / 1000) * COST_PER_KM, 2)


# =========================================================
# ⏱ Estimate duration
# =========================================================
def estimate_duration(distance_m):
    avg_speed_kmph = 40
    return (distance_m / 1000) / avg_speed_kmph * 60


# =========================================================
# 🔥 MAIN FUNCTION
# =========================================================
def find_routes(source=None, source_coords=None, destination=None, algorithm="astar"):
    try:
        # 📍 Source
        if source_coords:
            pass
        elif source:
            source_coords = geocode_place(source)
        else:
            return {"error": "Source not provided"}

        # 📍 Destination
        if not destination:
            return {"error": "Destination not provided"}

        dest_coords = geocode_place(destination)

        G = get_graph()
        orig, dest = get_nearest_nodes(G, source_coords, dest_coords)

        # =========================================================
        # 🚀 FAST MODE (A*)
        # =========================================================
        if algorithm == "astar":
            def heuristic(u, v):
             lat1 = G.nodes[u]["y"]
             lon1 = G.nodes[u]["x"]
             lat2 = G.nodes[v]["y"]
             lon2 = G.nodes[v]["x"]
             return ((lat1 - lat2)**2 + (lon1 - lon2)**2) ** 0.5
            
            path = nx.astar_path(
                    G,
                    orig,
                    dest,
                    heuristic=heuristic,
                    weight="length"
                )

            

            distance = nx.path_weight(G, path, weight="length")

            return {
                "algorithm": "astar",
                "route": nodes_to_coordinates(G, path),
                "distance": round(distance / 1000, 2),
                "duration": round(estimate_duration(distance), 2),
                "fuel_cost": calculate_fuel_cost(distance),
                "source": source_coords,
                "destination": dest_coords,
            }

        # =========================================================
        # 🧠 HYBRID MODE (A* + ALPHA-BETA)
        # =========================================================
        elif algorithm == "alpha_beta":

            paths = []

            try:
                # primary route
                main_path = nx.astar_path(G, orig, dest, weight="length")
                paths.append(main_path)

                # alternative route
                alt_path = nx.shortest_path(G, orig, dest, weight="length")
                if alt_path != main_path:
                    paths.append(alt_path)

            except Exception:
                return {"error": "Route generation failed"}

            routes_data = []

            for path in paths:
                distance = nx.path_weight(G, path, weight="length")

                routes_data.append({
                    "path": path,
                    "distance": distance,
                    "fuel": calculate_fuel_cost(distance),
                    "time": estimate_duration(distance)
                })

            # 🔥 Alpha-Beta (decision layer)
            def evaluate(route):
                return -(0.5 * route["distance"] +
                         0.3 * route["time"] +
                         0.2 * route["fuel"])

            def alpha_beta_routes(routes, depth, alpha, beta, maximizing):

                if depth == 0 or len(routes) == 1:
                    return evaluate(routes[0]), routes[0]

                if maximizing:
                    best = (-math.inf, None)

                    for i, route in enumerate(routes):
                        score, _ = alpha_beta_routes(
                            routes[i:], depth - 1, alpha, beta, False
                        )

                        if score > best[0]:
                            best = (score, route)

                        alpha = max(alpha, score)
                        if beta <= alpha:
                            break

                    return best

                else:
                    best = (math.inf, None)

                    for i, route in enumerate(routes):
                        score, _ = alpha_beta_routes(
                            routes[i:], depth - 1, alpha, beta, True
                        )

                        if score < best[0]:
                            best = (score, route)

                        beta = min(beta, score)
                        if beta <= alpha:
                            break

                    return best

            best_score, best_route = alpha_beta_routes(
                routes_data,
                depth=2,
                alpha=-math.inf,
                beta=math.inf,
                maximizing=True
            )

            return {
                "algorithm": "hybrid_alpha_beta",
                "route": nodes_to_coordinates(G, best_route["path"]),
                "distance": round(best_route["distance"] / 1000, 2),
                "duration": round(best_route["time"], 2),
                "fuel_cost": best_route["fuel"],
                "source": source_coords,
                "destination": dest_coords,
            }

        else:
            return {"error": "Invalid algorithm selected"}

    except Exception as e:
        print("❌ ERROR:", str(e))
        return {"error": str(e)}