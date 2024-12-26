import cfg
import uuid
import os

class VideoFiles:
    """
    Guarda la col·lecció d'arxius MP4
    """

    def __init__(self):
        self.root_dir = cfg.ROOT_DIR
        self.current_files = set()
        self.previous_files = set()

    def reload_fs(self, path: str):
        """ Recarrega la llista de fitxers MP4 des del disc. """
        self.previous_files = self.current_files.copy()
        self.current_files = set()

        for root, dirs, files in os.walk(path):
            for filename in files:
                if filename.lower().endswith('.mp4'):
                    absolute_path = os.path.abspath(os.path.join(root, filename))
                    self.current_files.add(absolute_path)

    def files_added(self) -> list:
        """ Retorna fitxers afegits després de la recàrrega. """
        return list(self.current_files - self.previous_files)

    def files_removed(self) -> list:
        """ Retorna fitxers eliminats després de la recàrrega. """
        return list(self.previous_files - self.current_files)

    def __len__(self):
        """ Retorna la quantitat de fitxers MP4 emmagatzemats. """
        return len(self.current_files)

    def __str__(self):
        """ Representació en cadena de VideoFiles. """
        return f"VideoFiles with {len(self)} files"



    def __repr__(self):
        return f"VideoFiles(current_files={len(self.current_files)})"

    def __len__(self):
        return len(self.current_files)

    def __iter__(self):
        return iter(self.current_files)
