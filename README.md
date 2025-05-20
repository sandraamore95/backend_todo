# Backend - Servidor FastAPI

Servidor backend para la aplicación de gestión de tareas, desarrollado con FastAPI.

## Características

- API RESTful completa
- Validación de datos con Pydantic
- Almacenamiento persistente en JSON
- Manejo de errores robusto
- CORS configurado
- Prevención de duplicados

## Estructura

```
backend/
├── server.py         # Servidor principal
├── requirements.txt  # Dependencias
└── todos.json       # Almacenamiento de tareas
```

## Endpoints

- `GET /api/todos` - Obtener todas las tareas
- `POST /api/todos` - Crear nueva tarea
- `PUT /api/todos/{id}` - Actualizar tarea
- `DELETE /api/todos/{id}` - Eliminar tarea

## Modelos de Datos

### Todo
```python
class Todo(BaseModel):
    id: Optional[int]
    text: str
    completed: bool
```

### TodoUpdate
```python
class TodoUpdate(BaseModel):
    text: Optional[str]
    completed: Optional[bool]
```

## Instalación

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Ejecutar el servidor:
```bash
python server.py
```

El servidor se ejecutará en `http://localhost:8000` 