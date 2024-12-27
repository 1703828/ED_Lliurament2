# -*- coding: utf-8 -*-
#PlayList.py : ** REQUIRED ** El vostre codi de la classe PlayList.

import cfg # Necessari per a la pràctica !!
 # Mireu el contingut de l'arxiu
import os.path
import sys
import numpy # installed in anaconda by default
import uuid
import vlc # $ pip install python-vlc
import time 
import os

class PlayList:
   
    def __init__ (self, video_id, video_player):
       
        self._videoid = video_id
        self._videoplayer = video_player
        self._playlist = []
    
    __slots__='_videoid','_videoplayer','_playlist'
   
    def load_file (self, file:str):
        self._playlist = []
        if not file.endswith(".m3u"):
            return
                
        with open(file, "r", errors = 'ignore') as fitxer:
            for linia in fitxer:
                linia = linia.strip()
                if linia and not linia.startswith("#") and linia.endswith(".mp4"):
                    uuid = self._videoid.get_uuid(linia)
                    if uuid:
                        self._playlist.append(uuid)
       
        return self._playlist
           
       
       

    def play(self, mode= int):
        if self._playlist:
            for uuid in self._playlist:
                self._videoplayer.play_video(uuid,mode)
   
    def add_video_at_end(self,uuid: str):
        self._playlist.append(uuid)
       

    def remove_first_video (self):
        if self._playlist:
            del self._playlist[0]
   
    def remove_last_video(self):
        if self._playlist:
            self._playlist.pop()
   
   
    def __len__(self):
        return len(self._playlist)
    
    def __iter__(self):
        return iter(self._playlist)
    
    def __str__(self):
        return str(self._playlist)
