from time import perf_counter

from fastapi import FastAPI
from app.database import connect_db
from app.routes import router

app = FastAPI()

# Conectar a la base de datos al iniciar la aplicación
connect_db()

# Registrar las rutas
app.include_router(router)

@app.get("/")
async def root():
    return {"message": "API de Sugerencias de Películas"}

@app.get("/happy-path")
async def happy_path():
    """
    Endpoint con una respuesta rápida para el Happy Path.
    """

    start_time = perf_counter()  # Inicia el temporizador
    response = {"message": "Todo está bien"}  # Respuesta del Happy Path
    latency = (perf_counter() - start_time) * 1000  # Calcula la latencia en ms
    response["latency"] = f"{latency:.3f}ms"  # Agrega la latencia como parte de la respuesta
    return response
