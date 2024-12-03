from motor.motor_asyncio import AsyncIOMotorClient

client = None
db = None

def connect_db():
    """
    Establece la conexión con MongoDB y asigna la base de datos global.
    """
    global client, db
    try:
        if client is None:  # Evita conexiones duplicadas
            client = AsyncIOMotorClient("mongodb://localhost:27017")
            db = client["movies"]  # Base de datos `movies`
            print("Conexión a MongoDB establecida.")
    except Exception as e:
        print(f"Hubo un fallo en la conexión: {e}")

def get_db():
    """
    Devuelve la referencia a la base de datos `movies`.
    """
    if db is None:  # Usar `is None` para evitar problemas
        raise ConnectionError("No hay conexión con la base de datos. Llama a `connect_db()` primero.")
    return db
