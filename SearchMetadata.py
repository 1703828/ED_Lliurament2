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
    __slots__ = ['__video_data']

    def __init__(self, obj_video_data: VideoData):
        self.__video_data = obj_video_data

    def get_similar(self, uuid: str, max_list: int) -> list:
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

    def get_auto_play(self, length: int) -> list:
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
            similar_videos.update(self.get_similar(uuid, length // 2))

        # Paso 3: Unión y ordenación por ranking
        combined_videos = list(set(top_videos) | similar_videos)
        combined_videos.sort(key=lambda x: (-self.__video_data.get_video_rank(x), x))

        # Paso 4: Calcular la similitud individual
        similarity_scores = {}
        for uuid in combined_videos:
            similarity_scores[uuid] = 0
            for other_uuid in combined_videos:
                if uuid != other_uuid:
                    similarity_scores[uuid] += self.get_similarity_score(uuid, other_uuid)

        # Paso 5: Ordenar por similitud total
        sorted_videos = sorted(similarity_scores.items(), key=lambda x: (-x[1], x[0]))

        # Paso 6: Retornar la lista final con valores None si faltan elementos
        final_list = [uuid for uuid, _ in sorted_videos[:length]]
        while len(final_list) < length:
            final_list.append(None)

        return final_list

    def get_similarity_score(self, uuid1: str, uuid2: str) -> float:
        """
        Calcula la similitud entre dos vídeos utilizando el algoritmo de similitud.
        """
        AB_nodes, AB_value = self.__video_data.get_video_distance(uuid1, uuid2)
        BA_nodes, BA_value = self.__video_data.get_video_distance(uuid2, uuid1)

        AB_sim = (AB_value / AB_nodes) * (self.__video_data.get_video_rank(uuid1) / 2) if AB_nodes > 0 else 0
        BA_sim = (BA_value / BA_nodes) * (self.__video_data.get_video_rank(uuid2) / 2) if BA_nodes > 0 else 0

        return AB_sim + BA_sim
