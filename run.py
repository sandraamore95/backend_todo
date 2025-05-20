import uvicorn
import os
import sys

# Obtener el directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))
# Agregar el directorio actual al path de Python
sys.path.insert(0, current_dir)

from app.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=[os.path.join(current_dir, "app")]
    ) 