from fastapi import APIRouter, HTTPException
from typing import List
from ..models.todo import Todo, TodoUpdate
from ..services.todo_service import TodoService
from ..utils.storage import JSONStorage

router = APIRouter()
storage = JSONStorage("todos.json")
todo_service = TodoService(storage)

@router.get("/todos", response_model=List[Todo])
async def get_todos():
    """Obtiene todas las tareas"""
    return todo_service.get_all()

@router.post("/todos", response_model=Todo)
async def create_todo(todo: Todo):
    """Crea una nueva tarea"""
    try:
        return todo_service.create(todo)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, updates: TodoUpdate):
    """Actualiza una tarea existente"""
    try:
        return todo_service.update(todo_id, updates)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    """Elimina una tarea"""
    try:
        todo_service.delete(todo_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) 