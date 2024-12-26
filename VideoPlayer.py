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

    __slots__ = ('__video_data', )

    def __init__(self, video_data: VideoData):
        """
        Inicializa el reproductor de video con los datos de VideoData
        :param video_data: instancia de la clase VideoData
        """
        self.__video_data = video_data

    def play_video(self, uuid: str, mode: int):
        """
        Reproduce el video según el modo especificado:
            mode : 0 - Imprime los metadatos y reproduce el video
            mode : 1 - Reproduce el video (sin imprimir metadatos)
            mode : 2 - Reproduce solo el video
        :param uuid: identificador único del video
        :param mode: modo de reproducción
        """
        file_path = self.__get_file_path(uuid)
        if not file_path:
            print(f"No se encontró el archivo para el UUID: {uuid}")
            return

        # Imprimir metadatos si el modo lo requiere
        if mode == 0 or mode == 1:
            self.__print_video(uuid)

        # Reproducir el video si el modo lo requiere
        if mode == 1 or mode == 2:
            self.__play_file(file_path)

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
    def __play_file(file: str):
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
