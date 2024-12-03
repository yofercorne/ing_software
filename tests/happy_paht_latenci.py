from fastapi.testclient import TestClient
from main import app

def test_happy_path_latency():
    """
    Prueba que el Happy Path tenga una latencia inferior a 1ms.
    """
    client = TestClient(app)
    response = client.get("/happy-path")

    # Verifica el código de estado
    assert response.status_code == 200

    # Calcula la latencia desde los datos de la respuesta
    latency_ms = float(response.json()["latency"].replace("ms", ""))
    print("this is latenci happy_phath:",latency_ms)
    assert latency_ms < 1, f"La latencia fue de {latency_ms}ms, excediendo el límite de 1ms"
