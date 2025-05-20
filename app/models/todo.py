from pydantic import BaseModel
from typing import Optional

class Todo(BaseModel):
    """Modelo para representar una tarea"""
    id: Optional[int] = None
    text: str
    completed: bool = False

class TodoUpdate(BaseModel):
    """Modelo para actualizar una tarea"""
    text: Optional[str] = None
    completed: Optional[bool] = None 