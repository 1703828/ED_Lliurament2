# -*- coding: utf-8 -*-
"""
VideoFiles.py : ** REQUIRED ** El vostre codi de la classe VideoFiles.
"""

import cfg
import os

class VideoFiles:
    """
    Guarda la col·lecció d'arxius MP4
    """

    def __init__(self):
        self.root_dir = cfg.ROOT_DIR
        self.current_files = set()
        self.previous_files = set()

    def _get_relative_path(self, absolute_path: str) -> str:
        """Converteix un path absolut a un path relatiu al directori arrel."""
        return os.path.relpath(absolute_path, self.root_dir)

    def reload_fs(self, path: str = None):
        """Recarrega la llista de fitxers MP4 des del disc."""
        path = path or self.root_dir
        self.previous_files = self.current_files.copy()
        self.current_files = set()
    
        print(f"[DEBUG] Recarregant els fitxers des del directori: {path}")  # Depuración
    
        for root, dirs, files in os.walk(path):
            for filename in files:
                if filename.lower().endswith('.mp4'):
                    absolute_path = os.path.abspath(os.path.join(root, filename))
                    relative_path = self._get_relative_path(absolute_path)
                    print(f"[DEBUG] Afegint fitxer: {relative_path}")  # Depuración
                    self.current_files.add(relative_path)
    
       

    def files_added(self) -> list:
        """Retorna fitxers afegits després de la recàrrega."""
        return sorted(self.current_files - self.previous_files)

    def files_removed(self) -> list:
        """Retorna fitxers eliminats després de la recàrrega."""
        return sorted(self.previous_files - self.current_files)

    def __len__(self):
        """Retorna la quantitat de fitxers MP4 emmagatzemats."""
        return len(self.current_files)

    def __str__(self):
        """Representació en cadena de VideoFiles."""
        return f"VideoFiles amb {len(self)} fitxers MP4"

    def __repr__(self):
        return f"VideoFiles(current_files={len(self.current_files)})"

    def __iter__(self):
        return iter(sorted(self.current_files))

    def __hash__(self):
        return hash(frozenset(self.current_files))
    def __eq__(self, other):
        if not isinstance(other, VideoFiles):
            return False
        return self.current_files == other.current_files
        
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __lt__(self, other):
        if not isinstance(other, VideoFiles):
            return False
        return len(self.current_files) < len(other.current_files)



