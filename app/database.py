from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure

client: AsyncIOMotorClient | None = None
database: AsyncIOMotorClient | None = None


async def connect_db(uri: str = "mongodb://localhost:27017", db_name: str = "concert_tickets"):
    """
    Establece la conexión con MongoDB y asigna la base de datos global.

    Args:
        uri (str): URI de conexión a MongoDB.
        db_name (str): Nombre de la base de datos a utilizar.
    """
    global client, database
    try:
        if client is None:  # Evita conexiones duplicadas
            client = AsyncIOMotorClient(uri, serverSelectionTimeoutMS=5000)  # Agregar timeout para evitar bloqueos
            # Verifica la conexión antes de asignar la base de datos
            await client.admin.command("ping")
            database = client[db_name]
            print(f"Conexión a MongoDB establecida con la base de datos '{db_name}'.")
        else:
            print("Ya existe una conexión activa con MongoDB.")
    except ConnectionFailure as e:
        print(f"Error de conexión a MongoDB: {e}")
        raise ConnectionError("No se pudo conectar a MongoDB. Verifica la URI y que el servidor esté activo.") from e
    except Exception as e:
        print(f"Hubo un error inesperado al conectar con MongoDB: {e}")
        raise RuntimeError("Error desconocido al intentar conectar con MongoDB.") from e


def get_db():
    """
    Devuelve la referencia a la base de datos global.

    Returns:
        database: Referencia a la base de datos global.

    Raises:
        ConnectionError: Si no hay conexión con la base de datos.
    """
    if database is None:
        raise ConnectionError(
            "No hay conexión con la base de datos. Llama a `connect_db()` primero."
        )
    return database


async def close_db():
    """
    Cierra la conexión con MongoDB.
    """
    global client, database
    try:
        if client:
            client.close()
            print("Conexión con MongoDB cerrada.")
            client = None
            database = None
        else:
            print("No hay una conexión activa para cerrar.")
    except Exception as e:
        print(f"Hubo un error al cerrar la conexión con MongoDB: {e}")
        raise RuntimeError("Error al intentar cerrar la conexión con MongoDB.") from e
