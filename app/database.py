from motor.motor_asyncio import AsyncIOMotorClient

client = None
database = None

async def connect_db():
    """
    Establece la conexión con MongoDB y asigna la base de datos global.
    """
    global client, database
    try:
        if client is None:  # Evita conexiones duplicadas
            client = AsyncIOMotorClient("mongodb://localhost:27017")
            database = client["concert_tickets"]  # Base de datos `concert_tickets`
            print("Conexión a MongoDB establecida.")
    except Exception as e:
        print(f"Hubo un fallo en la conexión a MongoDB: {e}")
        raise e

def get_db():
    """
    Devuelve la referencia a la base de datos `concert_tickets`.
    """
    if database is None:
        raise ConnectionError(
            "No hay conexión con la base de datos. Llama a `connect_db()` primero."
        )
    return database
