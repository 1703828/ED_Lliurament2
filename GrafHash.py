import cfg
import math
import copy
from ElementData import ElementData
from collections import defaultdict

class GrafHash:
    """Graf amb Adjacency Map structure."""
    __slots__ = ["__nodes","__out","__in"]
    
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
        
        def __str__(self):
            return str(self.__value)


        def get_element_data(self):
            return self.__value


    def __init__(self, ln=[],lv=[],lp=[],digraf=False):
        self.__nodes = {}  # Store vertices
        self.__out = {}  # Store outgoing edges
        self.__in = {} if digraf else self.__out # Store incoming edges
        
        for n in ln:
            self.insert_vertex(n, n)
        if lp==[]:
            for v in lv:
                self.insert_edge(v[0],v[1])
        else:
            for vA,pA in zip(lv,lp):
                self.insert_edge(vA[0],vA[1],pA)
    
    def es_digraf(self):
        return self.__out!=self.__in

    def getOut(self):
        return self.__out

    def insert_vertex(self, key, e: ElementData):
        """ Insert a vertex into the graph with a given key and an ElementData instance. """
        if not isinstance(e, ElementData):
            raise TypeError(f"Expected e to be of type ElementData, but got {type(e)}. Key: {key}")
        if key in self.__nodes:  
            return self.__nodes[key]
        vertex = self.Vertex(e)  
        self.__nodes[key] = vertex
        self.__out[key] = {}  
        if self.es_digraf():  
            self.__in[key] = {}
        return vertex


    def insert_edge(self, key1, key2, weight=1):
        """ Insert an edge between two vertices with an optional weight. """
        self.__out[key1][key2] = weight
        self.__in[key2][key1] = weight

    def get(self, key) -> ElementData:
        """ Get the ElementData associated with the key. """
        if key not in self.__nodes:
            raise KeyError(f"Node {key} does not exist.")
        return self.__nodes[key].get_element_data()

    def __contains__(self, key):
        """ Check if a vertex exists in the graph. """
        return key in self.__nodes

    def __getitem__(self, key):
        """ Get the ElementData associated with the key. """
        if key in self.__nodes:
            return self.get(key)

    def __delitem__(self, key):
        """ Remove a vertex and its associated edges from the graph. """
        if key in self.__nodes:
            del self.__nodes[key]
            del self.__out[key]
            for arestes_out in self.__out.values():
                if key in arestes_out:
                    del arestes_out[key]
           
            if self.es_digraf():
                del self.__in[key]
                for arestes_in in self.__in.values():
                    if key in arestes_in:
                        del arestes_in[key]


    def __existeix_edge(self,n1,n2):
        if n2 in self.__out[n1]:
            return True
        else:
            return False
    
    def edges_out(self, x):
        return self.__out[x].__iter__()

    def edges_in(self, x):
        return self.__in[x].__iter__()
     
    def grauPesIn(self,x):
        if x not in self.__in:
            raise KeyError("El node no existeix")
        return sum(self.__in[x].values())
       
    def grauPesOut(self,x):
        if x not in self.__out:
            raise KeyError("El node no existeix")
        return sum(self.__out[x].values())

    def itera(self):
        return self.__nodes.keys().__iter__()
    
    def __iter__(self):
        return iter(self.__nodes)
    
        
    def edges(self,key):
        if key not in self.__nodes:
            raise KeyError(f"El node amb clau {key} no existeix.")
        return iter(self.__out[key].items())

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
            
    def minDistance(self, dist, visitats):
        node_min = None
        minim_dist = math.inf
        for node, distancia in dist.items():
            if node not in visitats and distancia < minim_dist:
                minim_dist = distancia
                node_min = node
        return node_min

    def dijkstra(self, n):
        dist = {nAux: math.inf for nAux in self.__out}
        visitats = set()
        predecessors = {}
        dist[n] = 0

        for _ in range(len(self.__nodes) - 1):
            node_min = self.minDistance(dist, visitats)
            if node_min is None:
                break
            visitats.add(node_min)
            if node_min in self.__out:
                for n2, p2 in self.__out[node_min].items():
                    if n2 not in visitats:
                        if dist[node_min] + p2 < dist[n2]:
                            predecessors[n2] = node_min
                            dist[n2] = dist[node_min] + p2

        return dist, predecessors

    def dijkstraModif(self, n1, n2):
        dist = {nAux: math.inf for nAux in self.__out}
        visitats = set()
        predecessors = {}
        dist[n1] = 0

        for _ in range(len(self.__nodes) - 1):
            node_min = self.minDistance(dist, visitats)
            if node_min is None or node_min == n2:
                break
            visitats.add(node_min)
            if node_min in self.__out:
                for nAux, pes in self.__out[node_min].items():
                    if nAux not in visitats:
                        if dist[node_min] + pes < dist[nAux]:
                            predecessors[nAux] = node_min
                            dist[nAux] = dist[node_min] + pes

        return dist, predecessors

    def camiMesCurt(self, n1, n2):
        path = []
        if n1 in self.__nodes and n2 in self.__nodes:
            dist, pred = self.dijkstraModif(n1, n2)
            if n2 in pred:
                node = n2
                while node is not None:
                    path.insert(0, node)
                    node = pred.get(node)
        return path or None
