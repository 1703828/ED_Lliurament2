# -*- coding: utf-8 -*-
"""
SearchMetadata.py : Clase SearchMetadata con `__slots__` y mejoras.
"""

import cfg
import os
import sys
import tinytag
import numpy
from VideoData import VideoData

class SearchMetadata:
    __slots__ = ['__video_data']

    def __init__(self, obj_video_data):
        if not isinstance(obj_video_data, VideoData):
            raise TypeError("Expected a VideoData instance")
        self.__video_data = obj_video_data

    @property
    def video_data(self):
        return self.__video_data

    def filter_by_attribute(self, attribute_getter, sub):
        result = []
        for uuid in self.video_data.metadata.keys():
            try:
                value = attribute_getter(uuid)
                if value and sub.lower() in str(value).lower():
                    result.append(uuid)
            except (AttributeError, KeyError) as e:
                print(f"Error al filtrar por atributo: {e}")
                continue
        return result

    def duration(self, min_duration, max_duration):
        """Filtra videos por duración dentro de un rango."""
        return [
            uuid for uuid in self.video_data.metadata.keys()
            if (duration := self.video_data.get_duration(uuid)) is not None and min_duration <= duration <= max_duration
        ]

    def title(self, sub):
        return self.filter_by_attribute(self.video_data.get_title, sub)


    def album(self, sub):
        return self.filter_by_attribute(self.video_data.get_album, sub)

    def artist(self, sub):
        return self.filter_by_attribute(self.video_data.get_artist, sub)

    def composer(self, sub):
        return self.filter_by_attribute(self.video_data.get_composer, sub)

    def genre(self, sub):
        return self.filter_by_attribute(self.video_data.get_genre, sub)

    def date(self, sub):
        return self.filter_by_attribute(lambda uuid: str(self.video_data.get_date(uuid)), sub)

    def comment(self, sub):
        return self.filter_by_attribute(self.video_data.get_comment, sub)

    def and_operator(self, list1, list2):
        """Operador lógico AND que retorna la intersección de dos listas."""
        if not list1 or not list2:
            return []  # Si alguna lista está vacía, no hay intersección
        return list(set(list1) & set(list2))
    
    def or_operator(self, list1, list2):
        """Operador lógico OR que retorna la unión de dos listas."""
        if not list1 and not list2:
            return []  # Si ambas listas están vacías, retornar vacío
        return list(set(list1) | set(list2))


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
        return f"VideoID managing {len(self)} UUIDs"

    def get_similar(self, uuid: str, max_list: int) -> list:
        similarities = []
        for other_uuid in self.__video_data:
            if uuid == other_uuid:
                continue
            AB_nodes, AB_value = self.__video_data.get_video_distance(uuid, other_uuid)
            BA_nodes, BA_value = self.__video_data.get_video_distance(other_uuid, uuid)

            AB_sim = (AB_value / AB_nodes) * (self.__video_data.get_video_rank(uuid) / 2) if AB_nodes > 0 else 0
            BA_sim = (BA_value / BA_nodes) * (self.__video_data.get_video_rank(other_uuid) / 2) if BA_nodes > 0 else 0

            similarity = AB_sim + BA_sim
            similarities.append((similarity, other_uuid))

        similarities.sort(key=lambda x: (-x[0], x[1]))
        return [uuid for _, uuid in similarities[:min(max_list, 25)]]

    def get_auto_play(self, length: int) -> list:
        if length <= 0:
            return []

        videos_ranked = [(self.__video_data.get_video_rank(uuid), uuid) for uuid in self.__video_data]
        videos_ranked.sort(key=lambda x: (-x[0], x[1]))
        top_videos = [uuid for _, uuid in videos_ranked[:min(length, 25)]]

        similar_videos = set()
        for uuid in top_videos:
            similar_videos.update(self.get_similar(uuid, length // 2))

        combined_videos = list(set(top_videos) | similar_videos)
        combined_videos.sort(key=lambda x: (-self.__video_data.get_video_rank(x), x))

        similarity_scores = {
            uuid: sum(
                self.get_similarity_score(uuid, other_uuid)
                for other_uuid in combined_videos if uuid != other_uuid
            )
            for uuid in combined_videos
        }

        sorted_videos = sorted(similarity_scores.items(), key=lambda x: (-x[1], x[0]))
        final_list = [uuid for uuid, _ in sorted_videos[:length]]
        while len(final_list) < length:
            final_list.append(None)

        return final_list

    def get_similarity_score(self, uuid1: str, uuid2: str) -> float:
        AB_nodes, AB_value = self.__video_data.get_video_distance(uuid1, uuid2)
        BA_nodes, BA_value = self.__video_data.get_video_distance(uuid2, uuid1)

        AB_sim = (AB_value / AB_nodes) * (self.__video_data.get_video_rank(uuid1) / 2) if AB_nodes > 0 else 0
        BA_sim = (BA_value / BA_nodes) * (self.__video_data.get_video_rank(uuid2) / 2) if BA_nodes > 0 else 0

        return AB_sim + BA_sim
    def search_complex(self, criteria):
        result = set(self.video_data.metadata.keys())  # Inicializamos con todos los elementos
        for criterion, value in criteria.items():
            if criterion == "duration":
                result &= set(self.duration(value[0], value[1]))  # Intersección de duración
            elif criterion == "title":
                result &= set(self.title(value))
            elif criterion == "album":
                result &= set(self.album(value))
            elif criterion == "artist":
                result &= set(self.artist(value))
            elif criterion == "composer":
                result &= set(self.composer(value))
            elif criterion == "genre":
                result &= set(self.genre(value))
            elif criterion == "date":
                result &= set(self.date(value))
            elif criterion == "comment":
                result &= set(self.comment(value))
        return list(result)
