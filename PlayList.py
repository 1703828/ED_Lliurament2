import cfg
from VideoID import VideoID
from VideoPlayer import VideoPlayer

class PlayList:
    __slots__ = ['_video_id', '_video_player', '_videos']

    def __init__(self, video_id: VideoID, video_player: VideoPlayer):
        """
        Inicializa la PlayList con instancias de VideoID y VideoPlayer.
        """
        self._video_id = video_id
        self._video_player = video_player
        self._videos = []  # Lista de UUIDs

    def load_file(self, file: str):
        """
        Carga vídeos desde un archivo M3U y los añade a la PlayList sin repeticiones.
        """
        if not file.endswith(".m3u"):
            return

        with open(file, "r", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and line.endswith(".mp4"):
                    uuid = self._video_id.get_uuid(line)
                    if uuid and uuid not in self._videos:
                        self._videos.append(uuid)

    def read_list(self, p_llista: list):
        """
        Carga vídeos desde una lista de UUIDs sin repeticiones.
        """
        for uuid in p_llista:
            if uuid not in self._videos:
                self._videos.append(uuid)

    def play(self, mode: int):
        """
        Reproduce los vídeos de la PlayList en el orden en que aparecen.
        """
        if self._videos:
            for uuid in self._videos:
                self._video_player.play_video(uuid, mode)

    def add_video_at_end(self, uuid: str):
        """
        Añade un vídeo al final de la PlayList si no está ya presente.
        """
        if uuid not in self._videos:
            self._videos.append(uuid)

    def remove_first_video(self):
        """
        Elimina el primer vídeo de la PlayList.
        """
        if self._videos:
            self._videos.pop(0)

    def remove_last_video(self):
        """
        Elimina el último vídeo de la PlayList.
        """
        if self._videos:
            self._videos.pop()

    def __len__(self):
        """
        Retorna la cantidad de vídeos en la PlayList.
        """
        return len(self._videos)

    def __iter__(self):
        """
        Retorna un iterador sobre los UUIDs en la PlayList.
        """
        return iter(self._videos)

    def __str__(self):
        """
        Retorna una representación en cadena de la PlayList.
        """
        return f"PlayList with {len(self)} videos: {self._videos}"
