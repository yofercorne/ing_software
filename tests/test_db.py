import pytest
from motor.motor_asyncio import AsyncIOMotorClient

@pytest.fixture
async def test_db():
    """
    Configura una conexión a MongoDB para pruebas de forma asíncrona.
    """
    client = AsyncIOMotorClient("mongodb://localhost:27017")  # Conexión al servidor MongoDB local
    test_db = client["test_db"]  # Crea una base de datos llamada `test_db`
    try:
        yield test_db  # Proporciona la base de datos para las pruebas
    finally:
        await client.drop_database("test_db")  # Limpia la base de datos después de las pruebas
        client.close()  # Cierra la conexión al cliente MongoDB

# Prueba de inserción de usuario.
@pytest.mark.asyncio
async def test_create_user(test_db):
    """
    Prueba que un usuario se inserta correctamente en la base de datos.
    """
    db = test_db  # Asigna la base de datos temporal a la variable `db`

    # Define los datos del usuario que se va a insertar
    user_data = {"name": "Kevin", "preferences": ["acción", "comedia"]}

    # Inserta el usuario en la colección `users` de la base de datos
    result = await db["users"].insert_one(user_data)
    assert result.inserted_id is not None  # Verifica que el ID generado no sea nulo

    # Recupera al usuario recién insertado usando su ID
    user = await db["users"].find_one({"_id": result.inserted_id})
    assert user is not None  # Verifica que el usuario existe en la base de datos
    assert user["name"] == "Kevin"  # Comprueba que el nombre del usuario es el esperado
    assert user["preferences"] == ["acción", "comedia"]  # Verifica que las preferencias coinciden
