import json
import os
from typing import List, Dict, Any
from ..config import settings

class JSONStorage:
    """Clase para manejar el almacenamiento en JSON"""
    
    def __init__(self, file_path: str = None):
        self.file_path = file_path or settings.STORAGE_FILE
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Asegura que el archivo JSON existe"""
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump([], f)
    
    def read(self) -> List[Dict[str, Any]]:
        """Lee todos los datos del archivo JSON"""
        with open(self.file_path, 'r') as f:
            return json.load(f)
    
    def write(self, data: List[Dict[str, Any]]):
        """Escribe datos en el archivo JSON"""
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_next_id(self) -> int:
        """Obtiene el siguiente ID disponible"""
        todos = self.read()
        if not todos:
            return 1
        return max(todo['id'] for todo in todos) + 1 