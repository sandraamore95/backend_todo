from typing import List, Optional
from ..models.todo import Todo, TodoUpdate
from ..utils.storage import JSONStorage

class TodoService:
    """Servicio para manejar las operaciones CRUD de tareas"""
    
    def __init__(self, storage: JSONStorage):
        self.storage = storage
    
    def get_all(self) -> List[Todo]:
        """Obtiene todas las tareas"""
        todos_data = self.storage.read()
        return [Todo(**todo) for todo in todos_data]
    
    def create(self, todo: Todo) -> Todo:
        """Crea una nueva tarea"""
        todos_data = self.storage.read()
        
        # Validar duplicados
        if any(t['text'] == todo.text for t in todos_data):
            raise ValueError("Ya existe una tarea con ese texto")
        
        # Asignar ID
        todo.id = self.storage.get_next_id()
        
        # Guardar
        todos_data.append(todo.dict())
        self.storage.write(todos_data)
        
        return todo
    
    def update(self, todo_id: int, updates: TodoUpdate) -> Todo:
        """Actualiza una tarea existente"""
        todos_data = self.storage.read()
        
        # Buscar tarea
        todo_index = next((i for i, t in enumerate(todos_data) if t['id'] == todo_id), None)
        if todo_index is None:
            raise ValueError(f"No se encontró la tarea con ID {todo_id}")
        
        # Actualizar campos
        todo = Todo(**todos_data[todo_index])
        update_data = updates.dict(exclude_unset=True)
        
        # Validar texto duplicado si se está actualizando
        if 'text' in update_data:
            if any(t['text'] == update_data['text'] and t['id'] != todo_id for t in todos_data):
                raise ValueError("Ya existe una tarea con ese texto")
        
        # Aplicar actualizaciones
        for key, value in update_data.items():
            setattr(todo, key, value)
        
        # Guardar cambios
        todos_data[todo_index] = todo.dict()
        self.storage.write(todos_data)
        
        return todo
    
    def delete(self, todo_id: int):
        """Elimina una tarea"""
        todos_data = self.storage.read()
        
        # Buscar y eliminar tarea
        todo_index = next((i for i, t in enumerate(todos_data) if t['id'] == todo_id), None)
        if todo_index is None:
            raise ValueError(f"No se encontró la tarea con ID {todo_id}")
        
        todos_data.pop(todo_index)
        self.storage.write(todos_data) 