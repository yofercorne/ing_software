import pytest
from httpx import AsyncClient
from main import app  # Asegúrate de que `app` está correctamente definido en main.py
from fastapi.testclient import TestClient

@pytest.mark.asyncio
async def test_create_user():
    """
    Prueba el endpoint para crear un usuario usando AAA.
    """
    # Arrange: Configura los datos necesarios para la prueba
    payload = {"name": "Kevin", "preferences": ["acción", "comedia"]}

    # Act: Llama al endpoint para crear un usuario
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/users/", json=payload)

    # Assert: Verifica que el resultado sea el esperado
    assert response.status_code == 200  # Verifica el código HTTP
    data = response.json()
    assert data["name"] == "Kevin"  # Verifica que el nombre sea correcto
    assert data["preferences"] == ["acción", "comedia"]  # Verifica las preferencias
    assert "id" in data  # Verifica que se genere un ID
@pytest.mark.asyncio
async def test_root():
    """
    Prueba el endpoint raíz usando AAA.
    """
    # Act: Llama al endpoint raíz
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")

    # Assert: Verifica que el resultado sea el esperado
    assert response.status_code == 200
    assert response.json() == {"message": "API de Sugerencias de Películas"}
