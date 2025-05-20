from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import json
import os
from datetime import datetime

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de datos
class Todo(BaseModel):
    id: Optional[int] = None
    text: str = Field(..., min_length=1, max_length=200)
    completed: bool = False

# Modelo para actualización
class TodoUpdate(BaseModel):
    text: Optional[str] = None
    completed: Optional[bool] = None

# Almacenamiento
STORAGE_FILE = "todos.json"

def get_todos() -> List[Todo]:
    try:
        if os.path.exists(STORAGE_FILE):
            with open(STORAGE_FILE, 'r', encoding='utf-8') as f:
                return [Todo(**todo) for todo in json.load(f)]
        return []
    except (json.JSONDecodeError, IOError) as e:
        raise HTTPException(status_code=500, detail=f"Error al leer las tareas: {str(e)}")

def save_todos(todos: List[Todo]):
    try:
        with open(STORAGE_FILE, 'w', encoding='utf-8') as f:
            json.dump([todo.dict() for todo in todos], f, ensure_ascii=False, indent=2)
    except IOError as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar las tareas: {str(e)}")

def is_duplicate(text: str, exclude_id: Optional[int] = None) -> bool:
    todos = get_todos()
    return any(
        todo.text.lower() == text.lower() and 
        (exclude_id is None or todo.id != exclude_id)
        for todo in todos
    )

# Rutas
@app.get("/api/todos")
async def get_all_todos():
    return get_todos()

@app.post("/api/todos", status_code=201)
async def add_todo(todo: Todo):
    if is_duplicate(todo.text):
        raise HTTPException(status_code=400, detail="Esta tarea ya existe")
    
    todos = get_todos()
    todo.id = int(datetime.now().timestamp() * 1000)
    todo.text = todo.text.strip()
    todo.completed = False
    todos.append(todo)
    save_todos(todos)
    return todo

@app.put("/api/todos/{todo_id}")
async def update_todo(todo_id: int, todo_update: TodoUpdate):
    todos = get_todos()
    todo_index = next((i for i, t in enumerate(todos) if t.id == todo_id), None)
    
    if todo_index is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    # Actualizar texto si se proporciona
    if todo_update.text is not None:
        if not todo_update.text.strip():
            raise HTTPException(status_code=400, detail="La tarea no puede estar vacía")
        
        if is_duplicate(todo_update.text, todo_id):
            raise HTTPException(status_code=400, detail="Esta tarea ya existe")
        
        todos[todo_index].text = todo_update.text.strip()
    
    # Actualizar estado completed si se proporciona
    if todo_update.completed is not None:
        todos[todo_index].completed = todo_update.completed
    
    save_todos(todos)
    return todos[todo_index]

@app.delete("/api/todos/{todo_id}", status_code=204)
async def delete_todo(todo_id: int):
    todos = get_todos()
    if not any(todo.id == todo_id for todo in todos):
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    todos = [todo for todo in todos if todo.id != todo_id]
    save_todos(todos)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 