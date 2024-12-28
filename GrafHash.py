import cfg
from ElementData import ElementData
from collections import defaultdict

class GrafHash:
    """Graf amb Adjacency Map structure."""

    class Vertex:
        __slots__ = ["__value"]

        def __init__(self, value):
            self.__value = value

        def __hash__(self):
            return hash(self.__value)

        def __eq__(self, other):
            if not isinstance(other, GrafHash.Vertex):
                return False
            return self.__value == other.__value

        def __repr__(self):
            return f"Vertex({repr(self.__value)})"

    def __init__(self):
        self.__nodes = {}  # Store vertices
        self.__out = {}  # Store outgoing edges
        self.__in = {}  # Store incoming edges

    def insert_vertex(self, key, e: ElementData):
        """ Insert a vertex into the graph with a given key and an ElementData instance. """
        if key in self.__nodes:
            raise KeyError(f"Vertex with key {key} already exists.")
        vertex = self.Vertex(e)
        self.__nodes[key] = vertex
        self.__out[key] = {}
        self.__in[key] = {}

    def insert_edge(self, key1, key2, weight=1):
        """ Insert an edge between two vertices with an optional weight. """
        if key1 not in self.__nodes or key2 not in self.__nodes:
            raise KeyError("Both keys must exist as vertices in the graph.")
        self.__out[key1][key2] = weight
        self.__in[key2][key1] = weight

    def get(self, key) -> ElementData:
        """ Get the ElementData associated with the key. """
        if key not in self.__nodes:
            raise KeyError(f"Vertex with key {key} does not exist.")
        return self.__nodes[key].__value

    def __contains__(self, key):
        """ Check if a vertex exists in the graph. """
        return key in self.__nodes

    def __getitem__(self, key):
        """ Get the ElementData associated with the key. """
        if key not in self.__nodes:
            raise KeyError(f"Vertex with key {key} does not exist.")
        return self.__nodes[key].__value

    def __delitem__(self, key):
        """ Remove a vertex and its associated edges from the graph. """
        if key not in self.__nodes:
            raise KeyError(f"Vertex with key {key} does not exist.")
        del self.__nodes[key]
        del self.__out[key]
        for edges in self.__out.values():
            edges.pop(key, None)
        del self.__in[key]
        for edges in self.__in.values():
            edges.pop(key, None)

    def __iter__(self):
        """ Iterate over the vertices in the graph. """
        return iter(self.__nodes)

    def __repr__(self):
        """ Representació en cadena del graf. """
        return f"GrafHash(vertices={list(self.__nodes.keys())})"
    
    def __str__(self):
        """ Representació en cadena de Grafhash. """
        return f"GrafHash managing {len(self)} vertices"

    def __len__(self):
        """ Return the number of vertices in the graph. """
        return len(self.__nodes)
        
    def __lt__(self, other):
        if not isinstance(other, GrafHash.Vertex):
            return False
        return self.__value < other.__value  # Ordenar por el valor del vértice
    
    def __ne__(self, other):
        return not self.__eq__(other)
        
    def existeix_arestes(self, key1, key2):
        """ Verifica si existe una arista entre dos vértices. """
        return key2 in self.__out.get(key1, {})

    def get_weight(self, key1, key2):
        """ Devuelve el peso de la arista entre dos vértices. """
        return self.__out.get(key1, {}).get(key2, None)

    def update_edge_weight(self, key1, key2, weight):
        """ Actualiza el peso de la arista entre dos vértices. """
        if key2 in self.__out.get(key1, {}):
            self.__out[key1][key2] = weight
            self.__in[key2][key1] = weight
        else:
            raise KeyError(f"No edge exists between {key1} and {key2}")
