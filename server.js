const express = require('express');
const cors = require('cors');
const { LocalStorage } = require('node-localstorage');
const app = express();
const port = 8000;

// Configurar localStorage
const localStorage = new LocalStorage('./scratch');

// Middleware
app.use(cors());
app.use(express.json());

// Función para obtener todos los todos
function getTodos() {
    const todos = localStorage.getItem('todos');
    return todos ? JSON.parse(todos) : [];
}

// Función para guardar todos los todos
function saveTodos(todos) {
    localStorage.setItem('todos', JSON.stringify(todos));
}

// Función para verificar si una tarea ya existe
function isDuplicate(text, excludeId = null) {
    const todos = getTodos();
    return todos.some(todo => 
        todo.text.toLowerCase() === text.toLowerCase() && 
        (!excludeId || todo.id !== excludeId)
    );
}

// Rutas
app.get('/api/todos', (req, res) => {
    const todos = getTodos();
    res.json(todos);
});

app.post('/api/todos', (req, res) => {
    const { text } = req.body;
    
    // Validar que el texto no esté vacío
    if (!text || !text.trim()) {
        return res.status(400).json({ 
            error: 'La tarea no puede estar vacía' 
        });
    }

    // Validar que no sea duplicada
    if (isDuplicate(text)) {
        return res.status(400).json({ 
            error: 'Esta tarea ya existe' 
        });
    }

    const todos = getTodos();
    const newTodo = {
        id: Date.now(),
        text: text.trim(),
        completed: false
    };
    todos.push(newTodo);
    saveTodos(todos);
    res.status(201).json(newTodo);
});

app.put('/api/todos/:id', (req, res) => {
    const id = parseInt(req.params.id);
    const { text, completed } = req.body;
    const todos = getTodos();
    const todoIndex = todos.findIndex(todo => todo.id === id);
    
    if (todoIndex === -1) {
        return res.status(404).json({ 
            error: 'Tarea no encontrada' 
        });
    }

    // Si se está actualizando el texto
    if (text !== undefined) {
        // Validar que el texto no esté vacío
        if (!text || !text.trim()) {
            return res.status(400).json({ 
                error: 'La tarea no puede estar vacía' 
            });
        }

        // Validar que no sea duplicada
        if (isDuplicate(text, id)) {
            return res.status(400).json({ 
                error: 'Esta tarea ya existe' 
            });
        }

        todos[todoIndex].text = text.trim();
    }

    // Si se está actualizando el estado
    if (completed !== undefined) {
        todos[todoIndex].completed = completed;
    }

    saveTodos(todos);
    res.json(todos[todoIndex]);
});

app.delete('/api/todos/:id', (req, res) => {
    const id = parseInt(req.params.id);
    const todos = getTodos();
    const filteredTodos = todos.filter(todo => todo.id !== id);
    saveTodos(filteredTodos);
    res.status(204).send();
});

app.listen(port, () => {
    console.log(`Servidor corriendo en http://localhost:${port}`);
}); 