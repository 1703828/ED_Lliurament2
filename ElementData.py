# -*- coding: utf-8 -*-
"""
ElementData.py : ** REQUIRED ** El vostre codi de la classe PlayList.
"""
import cfg
import os

class ElementData:
    __slots__ = ("_title", "_artist", "_album", "_composer", "_genre", "_date", "_comment", "_duration", "_filename")

    def __init__(self, title="", artist="", album="", composer="", genre="", date="", comment="", duration=0, filename=""):
        if not filename:  # Si el filename está vacío o es None
            raise ValueError("El 'filename' es obligatorio y no puede estar vacío.")
        self._title = title
        self._artist = artist
        self._album = album
        self._composer = composer
        self._genre = genre
        self._date = date
        self._comment = comment
        self._duration = duration
        self._filename = filename

    # Propiedades (sin setters, solo getters)
    @property
    def title(self):
        return self._title

    @property
    def artist(self):
        return self._artist

    @property
    def album(self):
        return self._album

    @property
    def composer(self):
        return self._composer

    @property
    def genre(self):
        return self._genre

    @property
    def date(self):
        return self._date

    @property
    def comment(self):
        return self._comment

    @property
    def duration(self):
        return self._duration

    @property
    def filename(self):
        return self._filename

    def __hash__(self):
        return hash(self._filename)

    def __eq__(self, other):
        if not isinstance(other, ElementData):
            return False
        return self._filename == other._filename

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return (f"ElementData(title={self._title}, artist={self._artist}, album={self._album}, "
                f"composer={self._composer}, genre={self._genre}, date={self._date}, "
                f"comment={self._comment}, duration={self._duration}, filename={self._filename})")

    def __str__(self):
        return f"ElementData(title={self._title}, artist={self._artist}, filename={self._filename})"

    def __len__(self):
        return 1
        
    def __lt__(self, other):
        if not isinstance(other, ElementData):
            return False
        return self._title < other._title
