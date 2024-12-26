from GrafHash import GrafHash
from ElementData import ElementData
from PlayList import PlayList

class VideoData:
    __slots__ = ['__graph']

    def __init__(self):
        self.__graph = GrafHash()

    def get_video_rank(self, uuid: str) -> int:
        """
        Calcula el ranking de un vídeo sumando los pesos de todas las aristas que entran y salen.
        """
        if uuid not in self.__graph:
            return 0

        # Suma de los pesos de las aristas salientes
        rank_out = sum(self.__graph.get_edges_out(uuid).values())

        # Suma de los pesos de las aristas entrantes
        rank_in = sum(self.__graph.get_edges_in(uuid).values())

        return rank_out + rank_in

    def get_next_videos(self, uuid: str):
        """
        Iterador de vídeos directamente conectados como sucesores del nodo dado.
        """
        if uuid not in self.__graph:
            return iter([])

        return iter(self.__graph.get_edges_out(uuid).items())

    def get_previous_videos(self, uuid: str):
        """
        Iterador de vídeos directamente conectados como predecesores del nodo dado.
        """
        if uuid not in self.__graph:
            return iter([])

        return iter(self.__graph.get_edges_in(uuid).items())

    def get_video_distance(self, uuid1: str, uuid2: str) -> (int, int):
        """
        Calcula la distancia mínima entre dos vídeos (número de aristas y suma de pesos).
        Si no hay camino, devuelve (0, 0).
        """
        if uuid1 not in self.__graph or uuid2 not in self.__graph:
            return 0, 0

        path = self.__graph.dijkstraModif(uuid1, uuid2)
        if path is None:
            return 0, 0

        edges = zip(path, path[1:])
        nodes_count = len(path) - 1
        total_weight = sum(self.__graph.get_weight(u, v) for u, v in edges)

        return nodes_count, total_weight
