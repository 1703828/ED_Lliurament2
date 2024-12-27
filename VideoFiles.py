# -*- coding: utf-8 -*-
"""
VideoFiles.py : ** REQUIRED ** El vostre codi de la classe VideoFiles.
"""
import cfg # Necessari per a la pràctica !!
 # Mireu el contingut de l'arxiu
import os.path
import sys
import numpy # installed in anaconda by default
import uuid
import vlc # $ pip install python-vlc
import time
import sys
import os

class VideoFiles():
   
    def __init__(self):
        self._llista=[]
        self._files_added=[]
        self._files_removed=[]
   
    __slots__= '_llista','_files_added','_files_removed'
   
    def reload_fs(self,root):
        afegits=[]
        self._files_added=[]
        self._files_removed=[]
        for root, dirs, files in os.walk(root):
            for filename in files:
                if filename.lower().endswith(tuple(['.mp4'])):
                    file = os.path.join(root, filename)
                    afegits.append(file)
                    if file not in self._llista:
                        self._llista.append(file)
                        self._files_added.append(file)
       
        for fitxer in self._llista:
            if fitxer not in afegits:
                self._files_removed.append(fitxer)
               
   

   
    def files_added(self):
        return self._files_added
   
   
    def files_removed(self):
        return self._files_removed
    def __len__(self):
        return len(self._llista)
    def __iter__(self):
        return iter(self._llista)
    def __repr__(self):
        return (f"VideoFiles(llista={self._llista}, "
                f"files_added={self._files_added}, "
                f"files_removed={self._files_removed})")
    def __str__(self):
        return (f"VideoFiles with {len(self._llista)} files, "
                f"{len(self._files_added)} added, "
                f"{len(self._files_removed)} removed")
                
