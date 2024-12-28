import uuid
import os

class VideoID:
    """
    Gestiona el parell file-path <-> UUID per a arxius MP4.
    """
    __slots__ = ['__file_uuid_map']

    def __init__(self):
        self.__file_uuid_map = {}

    def generate_uuid(self, file: str) -> str:
        """ Genera un nou UUID per a un arxiu si encara no existeix. """
        new_uuid = uuid.uuid5(uuid.NAMESPACE_URL, file)
        # Verificar si el UUID ja existeix directament
        if new_uuid in self.__file_uuid_map:
            print('COL·LISIÓ: Identificador utilitzat anteriorment, aquest UUID no serà utilitzat.')
        else:
            self.__file_uuid_map[new_uuid] = file
            return str(new_uuid)

    def get_uuid(self, file: str) -> str:
        """ Retorna el UUID associat a un fitxer, si existeix. """
        # Verificar si el fitxer existeix directament
        for uuid, f in self.__file_uuid_map.items():
            if f == file:
                return str(uuid)

    def remove_uuid(self, id_uuid: str):
        """ Elimina un UUID del sistema. """
        try:
            file_uuid = uuid.UUID(id_uuid)
        except ValueError:
            print(f"Error: '{id_uuid}' no és un UUID vàlid.")
            return
        # Verificar si el UUID existeix directament
        if file_uuid in self.__file_uuid_map:
            del self.__file_uuid_map[file_uuid]

    def __len__(self):
        """ Retorna el nombre d'UUIDs registrats. """
        return len(self.__file_uuid_map)

    def __str__(self):
        """ Representació en cadena de VideoID. """
        return f"VideoID managing {len(self)} UUIDs"
    
    def __iter__(self):
        """ Permet iterar sobre els UUIDs registrats. """
        return iter(self.__file_uuid_map.keys())
        
    def __repr__(self):
        """ Representació en cadena de VideoID. """
        return str(self.__file_uuid_map)
