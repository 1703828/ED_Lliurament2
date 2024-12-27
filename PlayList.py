import cfg
from tinytag import TinyTag
import vlc
import time
from VideoData import VideoData
from VideoID import VideoID
from VideoPlayer import VideoPlayer
import os
import numpy
import uuid

class PlayList:
    __slots__ = ['__video_id', '__video_player', '__videos']

    def __init__(self, obj_video_id: VideoID, obj_video_player: VideoPlayer):
        """
        Inicializa la PlayList con instancias de VideoID y VideoPlayer.
        """
        self.__video_id = obj_video_id
        self.__video_player = obj_video_player
        self.__videos = []  # Lista de UUIDs

    def __load_file(self, file: str):
        """
        Carga vídeos desde un archivo M3U y los añade a la PlayList sin repeticiones.
        """
        if not file.endswith(".m3u"):
            return

        with open(file, "r", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and line.endswith(".mp4"):
                    uuid = self.__video_id.get_uuid(line)
                    if uuid and uuid not in self.__videos:
                        self.__videos.append(uuid)

    def __read_list(self, p_llista: list):
        """
        Carga vídeos desde una lista de UUIDs sin repeticiones.
        """
        for uuid in p_llista:
            if uuid not in self.__videos:
                self.__videos.append(uuid)

    def __play(self, mode: int):
        """
        Reproduce los vídeos de la PlayList en el orden en que aparecen.
        """
        if self.__videos:
            for uuid in self.__videos:
                self.__video_player.play_video(uuid, mode)

    def __add_video_at_end(self, uuid: str):
        """
        Añade un vídeo al final de la PlayList si no está ya presente.
        """
        if uuid not in self.__videos:
            self.__videos.append(uuid)

    def __remove_first_video(self):
        """
        Elimina el primer vídeo de la PlayList.
        """
        if self.__videos:
            self.__videos.pop(0)

    def __remove_last_video(self):
        """
        Elimina el último vídeo de la PlayList.
        """
        if self.__videos:
            self.__videos.pop()

    def __len__(self):
        return len(self.__videos)

    def __iter__(self):
        """Devuelve un iterador sobre los UUIDs de los vídeos."""
        return iter(self.__videos)

    def __repr__(self):
        return f"PlayList with {len(self)} videos"

    # Métodos públicos
    def load_file(self, file: str):
        self.__load_file(file)

    def read_list(self, p_llista: list):
        self.__read_list(p_llista)

    def play(self, mode: int):
        self.__play(mode)

    def add_video_at_end(self, uuid: str):
        self.__add_video_at_end(uuid)

    def remove_first_video(self):
        self.__remove_first_video()

    def remove_last_video(self):
        self.__remove_last_video()
