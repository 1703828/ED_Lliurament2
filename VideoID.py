import uuid
import cfg
class VideoID:
    """
    Gestiona el parell file-path <-> UUID per a arxius MP4.
    """

    def __init__(self):
        self._file_uuid_map = {}

    def generate_uuid(self, file: str) -> str:
        """Genera un nou UUID per a un arxiu si encara no existeix."""
        if file in self._file_uuid_map:
            return self._file_uuid_map[file]  # Retorna el UUID existent

        new_uuid = str(uuid.uuid5(uuid.NAMESPACE_URL, file))

        if new_uuid in self._file_uuid_map.values():
            print(f"COL·LISIÓ: L'identificador {new_uuid} ja està en ús. Aquest arxiu no s'utilitzarà.")
            return None

        self._file_uuid_map[file] = new_uuid
        return new_uuid

    def get_uuid(self, file: str) -> str:
        """Retorna el UUID associat a un fitxer, si existeix."""
        return self._file_uuid_map.get(file, None)

    def remove_uuid(self, id_uuid: str):
        """Elimina un UUID del sistema."""
        file_to_remove = None

        for file, uuid_str in self._file_uuid_map.items():
            if uuid_str == id_uuid:
                file_to_remove = file
                break

        if file_to_remove:
            del self._file_uuid_map[file_to_remove]
        else:
            print(f"Error: '{id_uuid}' no està registrat com a UUID.")

    def __len__(self):
        """Retorna el nombre d'UUIDs registrats."""
        return len(self._file_uuid_map)

    def __str__(self):
        """Representació en cadena de VideoID."""
        return f"VideoID gestionant {len(self)} UUIDs"

    def __repr__(self):
        return f"VideoID(file_uuid_map={len(self._file_uuid_map)})"

    def __iter__(self):
        """Permet iterar pels UUIDs registrats."""
        return iter(self._file_uuid_map.values())

    def __hash__(self):
        """Retorna un valor hash basat en el conjunt d'UUIDs registrats."""
        return hash(frozenset(self._file_uuid_map.values()))

    def __eq__(self, other):
        """Compara si dos objectes VideoID són iguals en funció dels seus UUIDs associats."""
        if isinstance(other, VideoID):
            return self._file_uuid_map == other._file_uuid_map
        return False
    def __ne__(self, other):
        return not self.__eq__(other)
            
    def __lt__(self, other):
        if not isinstance(other, VideoID):
            return False
        return len(self._file_uuid_map) < len(other._file_uuid_map)

