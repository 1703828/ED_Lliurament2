# -*- coding: utf-8 -*-
"""
ElementData.py : ** REQUIRED ** El vostre codi de la classe PlayList.
"""
import cfg
import os

class ElementData:
    __slots__ = ['__title', '__artist', '__album', '__composer', '__genre', '__date', '__comment', '__duration', '__filename']
    
    def __init__(self, title="", artist="", album="", composer="", genre="", date="", comment="", duration=0, filename=""):
        self.__title = title
        self.__artist = artist
        self.__album = album
        self.__composer = composer
        self.__genre = genre
        self.__date = date
        self.__comment = comment
        self.__duration = duration
        self.__filename = filename
    
    def __repr__(self):
        return f"ElementData(title={self.__title}, artist={self.__artist}, album={self.__album}, filename={self.__filename})"
    
    def __eq__(self, other):
        # Comparar solo si 'other' es una instancia de ElementData y basarse en 'filename'
        if not isinstance(other, ElementData):
            return False
        return self.__filename == other.__filename

    def __ne__(self, other):
        # La desigualdad se invierte a partir de la comparación de igualdad
        return not self.__eq__(other)
    
    def __lt__(self, other):
        # Comparación lexicográfica de 'filename'
        if not isinstance(other, ElementData):
            return NotImplemented
        return self.__filename < other.__filename
    
    def __hash__(self):
        # Asegurarse de que el hash se basa en 'filename'
        return hash(self.__filename)

    # Propiedades (sin setters, solo getters)
    @property
    def title(self):
        return self.__title

    @property
    def artist(self):
        return self.__artist

    @property
    def album(self):
        return self.__album

    @property
    def composer(self):
        return self.__composer

    @property
    def genre(self):
        return self.__genre

    @property
    def date(self):
        return self.__date

    @property
    def comment(self):
        return self.__comment

    @property
    def duration(self):
        return self.__duration

    @property
    def filename(self):
        return self.__filename

    def __str__(self):
        return f"ElementData(title={self.__title}, artist={self.__artist}, filename={self.__filename})"

    # Métodos de iteración y longitud eliminados, ya que no parece que la clase se deba usar de esta manera.
    
    @staticmethod
    def get_metadata(uuid: str, attribute: str):
        try:
            video = self.__graph.get(uuid)  # Obtener el nodo del grafo
            if video:
                return getattr(video, attribute, None)
        except AttributeError:
            return None
