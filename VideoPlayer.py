import cfg
from tinytag import TinyTag
import vlc
import time
from VideoData import VideoData
import os


class VideoPlayer:
    """
    Clase para reproducir videos MP4.
    Utiliza VideoData para obtener la información necesaria.
    """

    __slots__ = ['__video_data']

    def __init__(self, video_data: VideoData):
        if not isinstance(video_data, VideoData):
            raise TypeError("Se requiere una instancia de VideoData.")
        self.__video_data = video_data

    def play_video(self, uuid: str, mode: int):
        """
        Reproduce un video en base al modo especificado:
        - mode 0: Imprime los metadatos y reproduce el video.
        - mode 1: Solo imprime los metadatos.
        - mode 2: Solo reproduce el video.
        """
        file_path = self.get_file_path(uuid)
        if not file_path:
            print(f"Archivo no encontrado para UUID: {uuid}")
            return

        if mode == 0 or mode == 1:
            self.print_video(uuid)

        if mode == 0 or mode == 2:
            self.play_file(file_path)

    def get_file_path(self, uuid: str):
        """Obtiene la ruta del archivo para un UUID."""
        if not self.__video_data.existeix_uuid(uuid):
            print(f"UUID no encontrado: {uuid}")
            return None
        return self.__video_data.get_path(uuid)

    def print_video(self, uuid: str):
        """Imprime los metadatos de un video."""
        if not self.__video_data.existeix_meta(uuid):
            print(f"No se encontraron metadatos para el UUID: {uuid}")
            return

        print("\nMetadatos del video:")
        attributes = {
            "Título": self.__video_data.get_title(uuid),
            "Álbum": self.__video_data.get_album(uuid),
            "Artista": self.__video_data.get_artist(uuid),
            "Compositor": self.__video_data.get_composer(uuid),
            "Género": self.__video_data.get_genre(uuid),
            "Fecha": self.__video_data.get_date(uuid),
            "Comentario": self.__video_data.get_comment(uuid),
            "Duración": f"{self.__video_data.get_duration(uuid)} segundos",
        }
        for attr, value in attributes.items():
            print(f"{attr}: {value}")

    @staticmethod
    def play_file(file: str):
        """Reproduce un archivo MP4 usando VLC."""
        if not os.path.exists(file):
            print(f"Error: El archivo {file} no existe.")
            return

        player = vlc.MediaPlayer(file)
        player.play()

        try:
            tag = TinyTag.get(file)
            duration = int(tag.duration) if tag.duration else 0
            print(f"Reproduciendo: {file} ({duration} segundos)")
            time.sleep(duration)
        except Exception as e:
            print(f"Error al calcular la duración: {e}")
        finally:
            player.stop()

    def play_all_videos(self):
        """Reproduce todos los videos disponibles en VideoData."""
        if len(self.__video_data) == 0:
            print("No hay videos para reproducir.")
            return

        for uuid in self.__video_data.metadata.keys():
            self.play_video(uuid, 0)
    
    def __repr__(self):
        """Representación en cadena de VideoPlayer."""
        video_count = len(self.__video_data.metadata)
        return f"VideoPlayer managing {video_count} video(s)"
