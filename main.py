from time import perf_counter
from fastapi import FastAPI
from app.database import connect_db, close_db
from app.routes import router

app = FastAPI()

# Evento al iniciar la aplicación
@app.on_event("startup")
async def startup_event():
    await connect_db()
    print("Conexión a la base de datos establecida.")

# Evento al cerrar la aplicación
@app.on_event("shutdown")
async def shutdown_event():
    await close_db()
    print("Conexión a la base de datos cerrada.")

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
