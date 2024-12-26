class GrafHash:
    """Graf amb Adjacency Map structure."""

    class Vertex:
        __slots__ = "_value"

        def __init__(self, value):
            self._value = value

        def __hash__(self):
            return hash(self._value)

        def __eq__(self, other):
            if not isinstance(other, GrafHash.Vertex):
                return False
            return self._value == other._value

        def __repr__(self):
            return f"Vertex({repr(self._value)})"

    def __init__(self):
        self._nodes = {}
        self._out = {}
        self._in = {}

    def insert_vertex(self, key, e: ElementData):
        if key in self._nodes:
            raise KeyError(f"Vertex with key {key} already exists.")
        vertex = self.Vertex(e)
        self._nodes[key] = vertex
        self._out[key] = {}
        self._in[key] = {}

    def insert_edge(self, key1, key2, weight=1):
        if key1 not in self._nodes or key2 not in self._nodes:
            raise KeyError("Both keys must exist as vertices in the graph.")
        self._out[key1][key2] = weight
        self._in[key2][key1] = weight

    def get(self, key) -> ElementData:
        if key not in self._nodes:
            raise KeyError(f"Vertex with key {key} does not exist.")
        return self._nodes[key]._value

    def __contains__(self, key):
        return key in self._nodes

    def __getitem__(self, key):
        return self.get(key)

    def __delitem__(self, key):
        if key not in self._nodes:
            raise KeyError(f"Vertex with key {key} does not exist.")
        del self._nodes[key]
        del self._out[key]
        for edges in self._out.values():
            edges.pop(key, None)
        del self._in[key]
        for edges in self._in.values():
            edges.pop(key, None)

    def __iter__(self):
        return iter(self._nodes.keys())

    def __repr__(self):
        return f"GrafHash(vertices={list(self._nodes.keys())})"
