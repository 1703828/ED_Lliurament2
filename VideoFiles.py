# -*- coding: utf-8 -*-
"""
VideoFiles.py : ** REQUIRED ** El vostre codi de la classe VideoFiles.
"""
import cfg  # Necessari per a la pràctica !!
import os.path
import sys
import numpy  # installed in anaconda by default
import uuid
import vlc  # $ pip install python-vlc
import time
import sys
import os

class VideoFiles():
    __slots__ = ['__llista', '__files_added', '__files_removed']

    def __init__(self):
        self.__llista = []
        self.__files_added = []
        self.__files_removed = []

    def reload_fs(self, root):
        afegits = []
        self.__files_added = []
        self.__files_removed = []  # Cambiado _files_removed a __files_removed
        for root_dir, dirs, files in os.walk(root):
            for filename in files:
                if filename.lower().endswith(tuple(['.mp4'])):
                    file = os.path.join(root_dir, filename)
                    afegits.append(file)
                    if file not in self.__llista:  # Cambiado _llista a __llista
                        self.__llista.append(file)  # Cambiado _llista a __llista
                        self.__files_added.append(file)  # Cambiado _files_added a __files_added

        for fitxer in self.__llista:  # Cambiado _llista a __llista
            if fitxer not in afegits:
                self.__files_removed.append(fitxer)  # Cambiado _files_removed a __files_removed

    def files_added(self):
        return self.__files_added  # Cambiado _files_added a __files_added

    def files_removed(self):
        return self.__files_removed  # Cambiado _files_removed a __files_removed

    def __len__(self):
        return len(self.__llista)  # Cambiado _llista a __llista

    def __iter__(self):
        return iter(self.__llista)  # Cambiado _llista a __llista

    def __repr__(self):
        return (f"VideoFiles(llista={self.__llista}, "
                f"files_added={self.__files_added}, "
                f"files_removed={self.__files_removed})")  # Cambiado _llista, _files_added, _files_removed a __llista, __files_added, __files_removed

    def __str__(self):
        return (f"VideoFiles with {len(self.__llista)} files, "
                f"{len(self.__files_added)} added, "
                f"{len(self.__files_removed)} removed")  # Cambiado _llista, _files_added, _files_removed a __llista, __files_added, __files_removed
