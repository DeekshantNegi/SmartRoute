import osmnx as ox
import networkx as nx
from itertools import islice
from app.core.cache import get_graph_from_cache, set_graph_in_cache

# 🔥 Fuel cost config
COST_PER_KM = 5


# ✅ FIX: convert MultiDiGraph → DiGraph
def convert_to_digraph(G):
    D = nx.DiGraph()

    for u, v, data in G.edges(data=True):
        weight = data.get("length", 1)

        if D.has_edge(u, v):
            if D[u][v]["length"] > weight:
                D[u][v]["length"] = weight
        else:
            D.add_edge(u, v, **data)

    return D


# 🌍 Convert place → coordinates
def geocode_place(place: str):
    lat, lon = ox.geocode(place)
    return [lat, lon]


# 🚀 Load graph ONCE (cached)
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

    # ✅ Convert MultiDiGraph → DiGraph
    G_simple = nx.DiGraph()

    for u, v, data in G.edges(data=True):
        weight = data.get("length", 1)

        if G_simple.has_edge(u, v):
            if G_simple[u][v]["length"] > weight:
                G_simple[u][v]["length"] = weight
        else:
            G_simple.add_edge(u, v, length=weight)

    # ✅ Copy nodes
    for node, data in G.nodes(data=True):
        G_simple.add_node(node, **data)

    # 🔥 CRITICAL FIX: copy graph metadata (CRS etc.)
    G_simple.graph = G.graph

    print("📊 Nodes in graph:", len(G_simple.nodes))

    set_graph_in_cache(key, G_simple)

    return G_simple


# 📍 Get nearest nodes
def get_nearest_nodes(G, source_coords, dest_coords):
    orig = ox.distance.nearest_nodes(G, source_coords[1], source_coords[0])
    dest = ox.distance.nearest_nodes(G, dest_coords[1], dest_coords[0])
    return orig, dest


# 🗺 Convert nodes → coordinates
def nodes_to_coordinates(G, route):
    return [[G.nodes[node]["x"], G.nodes[node]["y"]] for node in route]


# ⛽ Fuel cost
def calculate_fuel_cost(distance_m):
    return round((distance_m / 1000) * COST_PER_KM, 2)


# ⏱ Estimate duration
def estimate_duration(distance_m):
    avg_speed_kmph = 40
    return (distance_m / 1000) / avg_speed_kmph * 60


# 🔥 MAIN FUNCTION
def find_routes(source=None, source_coords=None, destination=None):
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

        # 🚀 3 routes
        paths_generator = nx.shortest_simple_paths(G, orig, dest, weight="length")
        paths = list(islice(paths_generator, 3))

        route_types = ["low", "medium", "high"]

        routes_data = {}
        distance_data = {}
        duration_data = {}
        fuel_cost_data = {}

        for i, path in enumerate(paths):
            route_type = route_types[i]

            distance = nx.path_weight(G, path, weight="length")

            routes_data[route_type] = nodes_to_coordinates(G, path)
            distance_data[route_type] = round(distance / 1000, 2)
            duration_data[route_type] = round(estimate_duration(distance), 2)
            fuel_cost_data[route_type] = calculate_fuel_cost(distance)

        return {
            "routes": routes_data,
            "distance": distance_data,
            "duration": duration_data,
            "fuel_cost": fuel_cost_data,
            "source": source_coords,
            "destination": dest_coords,
        }

    except Exception as e:
        print("❌ ERROR:", str(e))
        return {"error": str(e)}