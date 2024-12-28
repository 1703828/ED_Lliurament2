# -*- coding: utf-8 -*-
# PlayList.py : ** REQUIRED ** El vostre codi de la classe PlayList.

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
   
    __slots__=['__videoid','__videoplayer','__playlist']

    def __init__(self, video_id, video_player):
        self.__videoid = video_id
        self.__videoplayer = video_player
        self.__playlist = []
    

    def load_file(self, file: str):
        self.__playlist = []
        if not file.endswith(".m3u"):
            return
                
        with open(file, "r", errors='ignore') as fitxer:
            for linia in fitxer:
                linia = linia.strip()
                if linia and not linia.startswith("#") and linia.endswith(".mp4"):
                    uuid = self.__videoid.get_uuid(linia)
                    if uuid:
                        self.__playlist.append(uuid)
       
        return self.__playlist
           
    def play(self, mode=int):
        if self.__playlist:
            for uuid in self.__playlist:
                self.__videoplayer.play_video(uuid, mode)
   
    def add_video_at_end(self, uuid: str):
        self.__playlist.append(uuid)
   
    def remove_first_video(self):
        if self.__playlist:
            del self.__playlist[0]
   
    def remove_last_video(self):
        if self.__playlist:
            self.__playlist.pop()
   
    def __len__(self):
        return len(self.__playlist)
    
    def __iter__(self):
        return iter(self.__playlist)
    
    def __str__(self):
        return str(self.__playlist)
    
    def __repr__(self):
        return self.__playlist
