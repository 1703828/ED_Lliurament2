# -*- coding: utf-8 -*-
# PlayList.py : ** REQUIRED ** El vostre codi de la classe PlayList.

import cfg 
import os.path
import sys
import numpy 
import uuid
import vlc
import time 
import os
from VideoID import VideoID  # Asegúrate de que la ruta sea correcta
from VideoPlayer import VideoPlayer  # Asegúrate de que la ruta sea correcta


class PlayList:
    __slots__ = ['__videoid', '__videoplayer', '__playlist']

    def __init__(self, video_id=None, video_player=None):
        # Verificar si los argumentos son válidos
        if video_id is None or not isinstance(video_id, VideoID):
            raise NotImplementedError("Se requiere una instancia válida de VideoData para video_id.")
        if video_player is None or not isinstance(video_player, VideoPlayer):
            raise NotImplementedError("Se requiere una instancia válida de VideoPlayer para video_player.")
        
        # Inicializar los atributos
        self.__videoid = video_id
        self.__videoplayer = video_player
        self.__playlist = []


    def load_file(self, file: str):
        self.__playlist = []
        if not file.endswith(".m3u"):
            return
                    
        with open(file, "r", errors='ignore') as fitxer:
            for linia in fitxer:
                linia = linia.strip()
                if linia and not linia.startswith("#") and linia.endswith(".mp4"):
                    uuid = self.__videoid.get_uuid(linia)
                    if uuid and uuid not in self.__playlist:
                        self.__playlist.append(uuid)
        
        return self.__playlist

    def read_list(self, p_llista: list):
        """Cargar vídeos desde una lista de UUIDs únicos."""
        self.__playlist = [uuid for uuid in p_llista if uuid not in self.__playlist]

    
    def play(self, mode=0):
        if not isinstance(mode, int):
            raise TypeError(f"El modo debe ser un entero, recibido: {type(mode)}")
        if self.__playlist:
            for uuid in self.__playlist:
                try:
                    self.__videoplayer.play_video(uuid, mode)
                except Exception as e:
                    print(f"Error al reproducir video {uuid}: {e}")

    def add_video_at_end(self, uuid: str):
        self.__playlist.append(uuid)
   
    def remove_first_video(self):
        if self.__playlist:
            del self.__playlist[0]
   
    def remove_last_video(self):
        if self.__playlist:
            self.__playlist.pop()
   
    def __len__(self):
        return len(self.__playlist)
    
    def __iter__(self):
        return iter(self.__playlist)
    
    def __str__(self):
        return str(self.__playlist)
    
    def __repr__(self):
        return self.__playlist
