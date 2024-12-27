from GrafHash import GrafHash
from ElementData import ElementData
import os
import sys
import tinytag
import numpy
import cfg

class VideoData:
    __slots__ = ['__graph', '__metadata']

    def __init__(self):
        self.__graph = GrafHash()
        self.__metadata = {}

    def get_video_rank(self, uuid: str) -> int:
        """ Calcula el ranking de un vídeo sumando los pesos de las aristas que entran y salen. """
        if not self.existeix_uuid(uuid):  # Verifica que el uuid esté presente
            return 0
    
        rank_out = sum(self.__graph.get_edges_out(uuid).values())  # Suma de los pesos de las aristas salientes
        rank_in = sum(self.__graph.get_edges_in(uuid).values())    # Suma de los pesos de las aristas entrantes
    
        return rank_out + rank_in
    
    def get_next_videos(self, uuid: str):
        """Iterador de vídeos directamente conectados como sucesores del nodo dado."""
        if not self.existeix_uuid(uuid):  # Verifica que el uuid exista
            return iter([])  # Si no existe, devuelve un iterador vacío
    
        return iter(self.__graph.get_edges_out(uuid).items())
    
    def get_previous_videos(self, uuid: str):
        """Iterador de vídeos directamente conectados como predecesores del nodo dado."""
        if not self.existeix_uuid(uuid):  # Verifica que el uuid exista
            return iter([])  # Si no existe, devuelve un iterador vacío
    
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

    def existeix_file(self, filename):
        """Verifica si un archivo ya existe en la metadata."""
        values = list(self.__metadata.values())
        files = [v[0] for v in values]
        return filename in files

    def add_video(self, uuid, filename):
        """Añade un video si no existe ya el archivo."""
        if not self.existeix_file(filename):
            if uuid and filename:  # Ambos valores no deben estar vacíos.
                root = cfg.get_root()
                path = os.path.realpath(os.path.join(root, filename))
                metadata = ElementData(filename=filename)
                self.__graph.insert_vertex(uuid, metadata)  # Añadimos el vídeo al grafo
                self.__metadata[uuid] = [filename, path]  # Guarda la metadata adicional

    def remove_video(self, uuid):
        """Elimina un video de la metadata usando su UUID."""
        if uuid in self.__metadata:
            self.__graph.__delitem__(uuid)  # Elimina el nodo del grafo
            del self.__metadata[uuid]

    def load_metadata(self, uuid):
        """Carga los metadatos desde un archivo MP4."""
        if uuid in self.__metadata:
            path = self.__metadata[uuid][1]
            metadata = tinytag.TinyTag.get(path)
            if metadata is None:
                print("ERROR: Archivo MP4 erróneo!")
                sys.exit(1)

            try:
                duration = int(numpy.ceil(metadata.duration))
            except AttributeError:
                duration = -1
            self.__metadata[uuid].append(duration)

            for attr, key in [
                ("title", "None"),
                ("album", "None"),
                ("artist", "None"),
                ("composer", "None"),
                ("genre", "None"),
                ("year", "None"),
                ("comment", "None"),
            ]:
                try:
                    value = getattr(metadata, attr, key)
                except AttributeError:
                    value = key
                self.__metadata[uuid].append(value)

            # Actualizamos la metadata en el grafo
            metadata_element = ElementData(
                title=self.__metadata[uuid][3],
                artist=self.__metadata[uuid][5],
                album=self.__metadata[uuid][4],
                composer=self.__metadata[uuid][6],
                genre=self.__metadata[uuid][7],
                date=self.__metadata[uuid][8],
                comment=self.__metadata[uuid][9],
                duration=self.__metadata[uuid][2],
                filename=self.__metadata[uuid][0]
            )
            self.__graph.get(uuid)._value = metadata_element  # Actualiza la instancia de ElementData

    def __len__(self):
        return len(self.__metadata)

    def existeix_uuid(self, uuid):
        """Verifica si un UUID existe en la metadata."""
        return uuid in self.__metadata.keys()

    def existeix_meta(self, uuid):
        """Verifica si un UUID tiene metadata completa."""
        if self.existeix_uuid(uuid):
            m = len(self.__metadata[uuid])
            return m > 2

    def __get_filename(self, uuid: str) -> str:
        """
        Devuelve el nombre de archivo asociado a un UUID si existe.
        """
        if self.existeix_meta(uuid):
            return self.__metadata[uuid][0]
        raise KeyError(f"No metadata found for UUID: {uuid}")
        
    def get_filename(self, uuid: str) -> str:
        return self.__get_filename(uuid)
        
    def get_path(self, uuid):
        """Devuelve la ruta del archivo asociada a un UUID."""
        if self.existeix_meta(uuid):
            return self.__metadata[uuid][1]

    def get_duration(self, uuid):
        """Devuelve la duración del video asociado a un UUID."""
        if self.existeix_meta(uuid):
            return self.__metadata[uuid][2]

    def get_title(self, uuid):
        """Devuelve el título del video asociado a un UUID."""
        if self.existeix_meta(uuid):
            return str(self.__metadata[uuid][3])

    def get_album(self, uuid):
        """Devuelve el álbum del video asociado a un UUID."""
        if self.existeix_meta(uuid):
            return str(self.__metadata[uuid][4])

    def get_artist(self, uuid):
        """Devuelve el artista del video asociado a un UUID."""
        if self.existeix_meta(uuid):
            return str(self.__metadata[uuid][5])

    def get_composer(self, uuid):
        """Devuelve el compositor del video asociado a un UUID."""
        if self.existeix_meta(uuid):
            return str(self.__metadata[uuid][6])

    def get_genre(self, uuid):
        """Devuelve el género del video asociado a un UUID."""
        if self.existeix_meta(uuid):
            return str(self.__metadata[uuid][7])

    def get_date(self, uuid):
        """Devuelve el año del video asociado a un UUID."""
        if self.existeix_meta(uuid):
            return str(self.__metadata[uuid][8])

    def get_comment(self, uuid):
        """Devuelve los comentarios del video asociado a un UUID."""
        if self.existeix_meta(uuid):
            return str(self.__metadata[uuid][9])

    @property
    def metadata(self):
        """Devuelve la metadata completa (solo lectura)."""
        return self.__metadata

    # 2.1
    def __repr__(self):
        return f"VideoData({len(self.__metadata)} videos)"

    def __iter__(self):
        """Devuelve un iterador sobre los UUIDs de los vídeos."""
        return iter(self.__metadata.keys())

    def __hash__(self):
        return hash(frozenset(self.__metadata.keys()))

    def __eq__(self, other):
        return isinstance(other, VideoData) and self.__metadata == other.__metadata

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return len(self) < len(other)

    def __str__(self):
        """ Representación en cadena de VideoData. """
        return f"VideoID managing {len(self)} UUIDs"
    
    # Función que procesa la lista de reproducción y añade las aristas
def read_playlist(self, obj_playlist: 'PlayList'):
    """
    Añade las aristas al grafo basándose en los vídeos consecutivos en una Playlist.
    Cada arista representa la relación de 'reproducción consecutiva' entre dos vídeos.
    El peso de la arista se incrementa si la secuencia se repite.
    """
    # Obtén la lista de vídeos de la PlayList
    videos = list(obj_playlist)
    
    if len(videos) < 2:
        print("ERROR: La playlist debe tener al menos dos vídeos.")
        return
    
    # Recorremos los vídeos consecutivos
    for i in range(len(videos) - 1):
        uuid1 = videos[i]
        uuid2 = videos[i + 1]
        
        if not self.existeix_uuid(uuid1) or not self.existeix_uuid(uuid2):  # Asegurarse de que ambos vídeos existan
            print(f"ERROR: Uno o ambos vídeos no existen en el grafo: {uuid1}, {uuid2}")
            continue

        # Si la arista ya existe, incrementamos su peso
        if self.__graph.existeix_arestes(uuid1, uuid2):
            weight = self.__graph.get_weight(uuid1, uuid2) + 1
            self.__graph.update_edge_weight(uuid1, uuid2, weight)
        else:
            # Si la arista no existe, la añadimos con peso 1
            self.__graph.insert_edge(uuid1, uuid2, 1)

