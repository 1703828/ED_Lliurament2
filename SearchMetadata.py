# -*- coding: utf-8 -*-
"""
SearchMetadata.py : ** REQUIRED ** El vostre codi de la classe SearchMetadata.
"""

import cfg
import os
import sys
import tinytag
import numpy
from VideoData import VideoData

class SearchMetadata:
    __slots__ = ['__video_data']  # Definimos los atributos de manera cerrada

    def __init__(self, obj_video_data: VideoData):
        """
        Inicializa la clase SearchMetadata con una instancia de VideoData.
        """
        if not isinstance(obj_video_data, VideoData):
            raise TypeError("Expected a VideoData instance")
        self.__video_data = obj_video_data  # Encapsulamos el atributo __video_data

    @property
    def video_data(self):
        """Getter para el atributo privado __video_data."""
        return self.__video_data

    def __duration(self, min_duration, max_duration):
        """Filtra los videos que están en el rango de duración [min_duration, max_duration]."""
        result = []
        for uuid in self.video_data.metadata.keys():  # Accedemos a los UUIDs desde la propiedad.
            try:
                duration = self.video_data.get_duration(uuid)
                if duration is not None and min_duration <= duration <= max_duration:
                    result.append(uuid)
            except AttributeError:
                continue
        return result

    def __title(self, sub):
        """Filtra los videos cuyo título contiene la subcadena 'sub'."""
        result = []
        for uuid in self.video_data.metadata.keys():
            try:
                title = self.video_data.get_title(uuid)
                if title and sub.lower() in title.lower():
                    result.append(uuid)
            except AttributeError:
                continue
        return result

    def __album(self, sub):
        """Filtra los videos cuyo álbum contiene la subcadena 'sub'."""
        result = []
        for uuid in self.video_data.metadata.keys():
            try:
                album = self.video_data.get_album(uuid)
                if album and sub.lower() in album.lower():
                    result.append(uuid)
            except AttributeError:
                continue
        return result

    def __artist(self, sub):
        """Filtra los videos cuyo autor contiene la subcadena 'sub'."""
        result = []
        for uuid in self.video_data.metadata.keys():
            try:
                artist = self.video_data.get_artist(uuid)
                if artist and sub.lower() in artist.lower():
                    result.append(uuid)
            except AttributeError:
                continue
        return result

    def __composer(self, sub):
        """Filtra los videos cuyo compositor contiene la subcadena 'sub'."""
        result = []
        for uuid in self.video_data.metadata.keys():
            try:
                composer = self.video_data.get_composer(uuid)
                if composer and sub.lower() in composer.lower():
                    result.append(uuid)
            except AttributeError:
                continue
        return result

    def __genre(self, sub):
        """Filtra los videos cuyo género contiene la subcadena 'sub'."""
        result = []
        for uuid in self.video_data.metadata.keys():
            try:
                genre = self.video_data.get_genre(uuid)
                if genre and sub.lower() in genre.lower():
                    result.append(uuid)
            except AttributeError:
                continue
        return result

    def __date(self, sub):
        """Filtra los videos cuya fecha contiene la subcadena 'sub'."""
        result = []
        for uuid in self.video_data.metadata.keys():
            try:
                date = str(self.video_data.get_date(uuid))
                if date and sub in date:
                    result.append(uuid)
            except AttributeError:
                continue
        return result

    def __comment(self, sub):
        """Filtra los videos cuyo comentario contiene la subcadena 'sub'."""
        result = []
        for uuid in self.video_data.metadata.keys():
            try:
                comment = self.video_data.get_comment(uuid)
                if comment and sub.lower() in comment.lower():
                    result.append(uuid)
            except AttributeError:
                continue
        return result

    def __and_operator(self, list1, list2):
        """Devuelve la intersección de dos listas de UUIDs (AND lógico)."""
        return list(set(list1) & set(list2))

    def __or_operator(self, list1, list2):
        """Devuelve la unión de dos listas de UUIDs (OR lógico)."""
        return list(set(list1) | set(list2))

    """
    Métodos adicionales (Parte 2)
    """

    def __repr__(self):
        return f"SearchMetadata(video_data={len(self.__video_data)} videos)"

    def __len__(self):
        return len(self.__video_data.metadata)

    def __iter__(self):
        return iter(self.__video_data.metadata.keys())

    def __hash__(self):
        return hash(id(self))

    def __eq__(self, other):
        return isinstance(other, SearchMetadata) and self.video_data.metadata == other.video_data.metadata

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return len(self) < len(other)

    def __str__(self):
        """ Representación en cadena de Searchmetadata. """
        return f"VideoID managing {len(self)} UUIDs"

    def __get_similar(self, uuid: str, max_list: int) -> list:
        """
        Retorna una lista de vídeos similares basada en el algoritmo de similitud definido.
        """
        similarities = []
        
        for other_uuid in self.__video_data:
            if uuid == other_uuid:
                continue

            # Calcula las distancias en ambas direcciones
            AB_nodes, AB_value = self.__video_data.get_video_distance(uuid, other_uuid)
            BA_nodes, BA_value = self.__video_data.get_video_distance(other_uuid, uuid)

            # Calcula la similitud para ambas direcciones
            AB_sim = (AB_value / AB_nodes) * (self.__video_data.get_video_rank(uuid) / 2) if AB_nodes > 0 else 0
            BA_sim = (BA_value / BA_nodes) * (self.__video_data.get_video_rank(other_uuid) / 2) if BA_nodes > 0 else 0

            similarity = AB_sim + BA_sim
            similarities.append((similarity, other_uuid))

        # Ordena por similitud y UUID
        similarities.sort(key=lambda x: (-x[0], x[1]))

        # Devuelve la lista limitada por max_list
        return [uuid for _, uuid in similarities[:min(max_list, 25)]]

    def __get_auto_play(self, length: int) -> list:
        """
        Genera una lista de reproducción automatizada basada en el ranking y similitud.
        """
        if length <= 0:
            return []

        # Paso 1: Obtener los vídeos con mayor ranking
        videos_ranked = [(self.__video_data.get_video_rank(uuid), uuid) for uuid in self.__video_data]
        videos_ranked.sort(key=lambda x: (-x[0], x[1]))
        top_videos = [uuid for _, uuid in videos_ranked[:min(length, 25)]]

        # Paso 2: Obtener los vídeos más similares a cada uno
        similar_videos = set()
        for uuid in top_videos:
            similar_videos.update(self.__get_similar(uuid, length // 2))

        # Paso 3: Unión y ordenación por ranking
        combined_videos = list(set(top_videos) | similar_videos)
        combined_videos.sort(key=lambda x: (-self.__video_data.get_video_rank(x), x))

        # Paso 4: Calcular la similitud individual
        similarity_scores = {}
        for uuid in combined_videos:
            similarity_scores[uuid] = 0
            for other_uuid in combined_videos:
                if uuid != other_uuid:
                    similarity_scores[uuid] += self.__get_similarity_score(uuid, other_uuid)

        # Paso 5: Ordenar por similitud total
        sorted_videos = sorted(similarity_scores.items(), key=lambda x: (-x[1], x[0]))

        # Paso 6: Retornar la lista final con valores None si faltan elementos
        final_list = [uuid for uuid, _ in sorted_videos[:length]]
        while len(final_list) < length:
            final_list.append(None)

        return final_list

    def __get_similarity_score(self, uuid1: str, uuid2: str) -> float:
        """
        Calcula la similitud entre dos vídeos utilizando el algoritmo de similitud.
        """
        AB_nodes, AB_value = self.__video_data.get_video_distance(uuid1, uuid2)
        BA_nodes, BA_value = self.__video_data.get_video_distance(uuid2, uuid1)

        AB_sim = (AB_value / AB_nodes) * (self.__video_data.get_video_rank(uuid1) / 2) if AB_nodes > 0 else 0
        BA_sim = (BA_value / BA_nodes) * (self.__video_data.get_video_rank(uuid2) / 2) if BA_nodes > 0 else 0

        return AB_sim + BA_sim
