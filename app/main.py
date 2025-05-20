from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import todos
from .config import settings

app = FastAPI(title=settings.APP_NAME)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(todos.router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)