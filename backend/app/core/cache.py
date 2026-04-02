import time

# Store graphs with timestamp
_graph_cache = {}

# Cache expiry time (in seconds)
CACHE_TTL = 60 * 60  # 1 hour


def _is_expired(timestamp):
    return (time.time() - timestamp) > CACHE_TTL


def get_graph_from_cache(key):
    """
    Get graph from cache if exists and not expired
    """
    if key in _graph_cache:
        graph, timestamp = _graph_cache[key]

        if not _is_expired(timestamp):
            return graph
        else:
            # Remove expired cache
            del _graph_cache[key]

    return None


def set_graph_in_cache(key, graph):
    """
    Store graph in cache with timestamp
    """
    _graph_cache[key] = (graph, time.time())


def clear_cache():
    """
    Clear all cache (useful for debugging)
    """
    _graph_cache.clear()