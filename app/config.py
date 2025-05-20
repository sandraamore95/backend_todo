class Settings:
    """Configuración de la aplicación"""
    APP_NAME: str = "Todo API"
    STORAGE_FILE: str = "todos.json"
    CORS_ORIGINS: list = ["*"]
    PORT: int = 8000
    HOST: str = "0.0.0.0"

settings = Settings() 