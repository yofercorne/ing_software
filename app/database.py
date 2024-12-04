from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure

client = None
database = None

async def connect_db(uri: str = "mongodb://localhost:27017", db_name: str = "concert_tickets"):
    """
    Conecta a la base de datos MongoDB.
    """
    global client, database
    try:
        if client is None:  # Evita conexiones duplicadas
            client = AsyncIOMotorClient(uri)
            await client.admin.command("ping")  # Prueba la conexión
            database = client[db_name]
            print(f"Conexión establecida a la base de datos: {db_name}")
    except ConnectionFailure as e:
        print(f"Error al conectar con la base de datos: {e}")
        raise ConnectionError("No se pudo conectar a la base de datos.")
    except Exception as e:
        print(f"Error inesperado: {e}")
        raise RuntimeError("Ocurrió un error inesperado al conectar a la base de datos.")

def get_db():
    """
    Obtiene la referencia a la base de datos.
    """
    if database is None:
        raise ConnectionError("No hay conexión con la base de datos. Llama a `connect_db()` primero.")
    return database

async def close_db():
    """
    Cierra la conexión con la base de datos.
    """
    global client
    if client:
        client.close()
        print("Conexión con MongoDB cerrada.")
        client = None
