
# -*- coding: utf-8 -*-
"""
GrafHash.py : ** REQUIRED ** El vostre codi de la classe PlayList.
"""
import cfg
from ElementData import ElementData
from collections import defaultdict


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
        self._nodes = {}  # Store vertices
        self._out = {}  # Store outgoing edges
        self._in = {}  # Store incoming edges

    def insert_vertex(self, key, e: ElementData):
        """ Insert a vertex into the graph with a given key and an ElementData instance. """
        if key in self._nodes:
            raise KeyError(f"Vertex with key {key} already exists.")
        vertex = self.Vertex(e)
        self._nodes[key] = vertex
        self._out[key] = {}
        self._in[key] = {}

    def insert_edge(self, key1, key2, weight=1):
        """ Insert an edge between two vertices with an optional weight. """
        if key1 not in self._nodes or key2 not in self._nodes:
            raise KeyError("Both keys must exist as vertices in the graph.")
        self._out[key1][key2] = weight
        self._in[key2][key1] = weight

    def get(self, key) -> ElementData:
        """ Get the ElementData associated with the key. """
        if key not in self._nodes:
            raise KeyError(f"Vertex with key {key} does not exist.")
        return self._nodes[key]._value

    def __contains__(self, key):
        """ Check if a vertex exists in the graph. """
        return key in self._nodes

    def __getitem__(self, key):
        """ Get the ElementData associated with the key. """
        return self.get(key)

    def __delitem__(self, key):
        """ Remove a vertex and its associated edges from the graph. """
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
        """ Iterate over the keys (vertices) in the graph. """
        return iter(self._nodes.keys())

    def __repr__(self):
        """ Representació en cadena del graf. """
        return f"GrafHash(vertices={list(self._nodes.keys())})"
    
    def __str__(self):
        """ Representació en cadena de Grafhash. """
        return f"GrafHash managing {len(self)} vertices"

    def __len__(self):
        """ Return the number of vertices in the graph. """
        return len(self._nodes)
        
    def __lt__(self, other):
        if not isinstance(other, GrafHash.Vertex):
            return False
        return self._value < other._value  # Ordenar por el valor del vértice
    
    def __ne__(self, other):
        return not self.__eq__(other)
        
    def existeix_arestes(self, key1, key2):
        """ Verifica si existe una arista entre dos vértices. """
        return key2 in self._out.get(key1, {})

    def get_weight(self, key1, key2):
        """ Devuelve el peso de la arista entre dos vértices. """
        return self._out.get(key1, {}).get(key2, None)

    def update_edge_weight(self, key1, key2, weight):
        """ Actualiza el peso de la arista entre dos vértices. """
        if key2 in self._out.get(key1, {}):
            self._out[key1][key2] = weight
            self._in[key2][key1] = weight
        else:
            raise KeyError(f"No edge exists between {key1} and {key2}")
