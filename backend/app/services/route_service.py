import osmnx as ox
import networkx as nx
from app.core.cache import get_graph_from_cache, set_graph_in_cache


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

    # 🔥 Fix nearest_nodes + performance
    

    print("📊 Nodes in graph:", len(G.nodes))

    set_graph_in_cache(key, G)

    return G


# 📍 Get nearest nodes
def get_nearest_nodes(G, source_coords, dest_coords):
    orig = ox.distance.nearest_nodes(G, source_coords[1], source_coords[0])
    dest = ox.distance.nearest_nodes(G, dest_coords[1], dest_coords[0])
    return orig, dest


# 🗺 Convert nodes → coordinates
def nodes_to_coordinates(G, route):
    return [[G.nodes[node]["x"], G.nodes[node]["y"]] for node in route]


# ⏱ Estimate duration
def estimate_duration(distance_m):
    avg_speed_kmph = 40
    return (distance_m / 1000) / avg_speed_kmph * 60


# 🔥 MAIN FUNCTION
def find_routes(source: str, destination: str):
    try:
        source_coords = geocode_place(source)
        dest_coords = geocode_place(destination)

        G = get_graph()

        orig, dest = get_nearest_nodes(G, source_coords, dest_coords)

        # 🚀 FAST ROUTE USING NETWORKX
        path = nx.shortest_path(G, orig, dest, weight="length")
        distance = nx.shortest_path_length(G, orig, dest, weight="length")

        coords = nodes_to_coordinates(G, path)

        return {
            "routes": {
                "low": coords,
                "medium": coords,
                "high": coords,
            },
            "distance": {
                "low": round(distance / 1000, 2),
                "medium": round(distance / 1000, 2),
                "high": round(distance / 1000, 2),
            },
            "duration": {
                "low": round(estimate_duration(distance), 2),
                "medium": round(estimate_duration(distance), 2),
                "high": round(estimate_duration(distance), 2),
            },
            "source": source_coords,
            "destination": dest_coords,
        }

    except Exception as e:
        return {"error": str(e)}