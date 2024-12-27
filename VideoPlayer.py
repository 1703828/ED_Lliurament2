# -*- coding: utf-8 -*-
"""
VideoPlayer.py : ** REQUIRED ** El vostre codi de la classe VideoPlayer.
"""
import cfg
import os
import time
import vlc
from tinytag import TinyTag
from VideoData import VideoData

class VideoPlayer:
    """
    Reproduir els vídeos dels MP4
    Ha d'utilitzar les altres classes per poder fer-ho, no guarda info,
    nomès actua
    """

    __slots__ = ['__video_data']

    def __init__(self, video_data: VideoData):
        """
        Inicializa el VideoPlayer con una instancia de VideoData.
        """
        self.__video_data = video_data



    def play_video(self, uuid: str, mode: int):
        """
        Reproduce un vídeo dado un UUID y un modo.
        
        Parameters:
        - uuid (str): Identificador único del vídeo a reproducir.
        - mode (int): El modo en que se debe reproducir el vídeo (por ejemplo, 1 para normal, 2 para repetición, etc.)
        """
        filename = self.__video_data.get_filename(uuid)
        file_path = self.__video_data.get_path(uuid)
        
        if not os.path.exists(file_path):
            print(f"Error: El archivo {filename} no se encuentra en la ruta {file_path}.")
            return
        
        media = vlc.Media(file_path)
        self.__player.set_media(media)
        
        if mode == 2:  # Supongamos que 'mode 2' es para repetición
            self.__player.set_playback_mode(vlc.MediaPlayer().loop)
        
        print(f"Reproduciendo: {filename} en modo {mode}")
        self.__player.play()

        while self.__player.is_playing():
            time.sleep(1)
            
    def __get_file_path(self, uuid: str):
        """
        Obtiene la ruta del archivo para un UUID
        :param uuid: identificador único del video
        :return: ruta del archivo o None si no se encuentra
        """
        if not self.__video_data.existeix_uuid(uuid):
            print(f"UUID no encontrado: {uuid}")
            return None
        return self.__video_data.get_path(uuid)

    def __print_video(self, uuid: str):
        """
        Imprime los metadatos de un video en pantalla.
        :param uuid: identificador único del video
        """
        if not self.__video_data.existeix_meta(uuid):
            print("No se encontraron metadatos para el UUID proporcionado.")
            return

        print(f"Título: {self.__video_data.get_title(uuid)}")
        print(f"Álbum: {self.__video_data.get_album(uuid)}")
        print(f"Artista: {self.__video_data.get_artist(uuid)}")
        print(f"Compositor: {self.__video_data.get_composer(uuid)}")
        print(f"Género: {self.__video_data.get_genre(uuid)}")
        print(f"Fecha: {self.__video_data.get_date(uuid)}")
        print(f"Comentario: {self.__video_data.get_comment(uuid)}")
        print(f"Duración: {self.__video_data.get_duration(uuid)} segundos")

    @staticmethod
# Cambio de __play_file() a play_file()
    def play_file(self, file: str):
        """
        Reproduce un archivo MP4.
        :param file: ruta del archivo a reproducir
        """
        if not os.path.exists(file):
            print(f"Error: El archivo {file} no existe.")
            return
    
        player = vlc.MediaPlayer(file)
        player.play()
    
        # Espera hasta que el video termine de reproducirse
        tag = TinyTag.get(file)
        duration = int(tag.duration) if tag.duration else 0
        time.sleep(duration)
        player.stop()

    def play_all_videos(self):
        """
        Reproduce todos los videos en la colección de datos.
        """
        if len(self.__video_data) == 0:
            print("No hay videos para reproducir.")
            return

        for uuid in self.__video_data:
            self.play_video(uuid, 1)  # Reproducir cada video con opción de mostrar metadatos
    
    def __str__(self):
        """ Representació en cadena de Videoplayer. """
        return f"VideoID managing {len(self)} UUIDs"
    def __len__(self):
        """ Retorna el nombre d'UUIDs registrats. """
        return len(self)
    def __repr__(self):
        """
        Devuelve una representación en cadena de VideoPlayer con el número de videos gestionados.
        """
        return f"VideoPlayer managing {len(self.__video_data)} videos"
