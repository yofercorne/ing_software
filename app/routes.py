# routes.py
from fastapi import APIRouter, HTTPException
from app.schemas import UserCreate, UserResponse, MovieCreate, MovieResponse
from app.database import get_db
from bson import ObjectId

router = APIRouter()

@router.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate):
    """
    Crea un usuario en la base de datos (Basico).
    """
    try:
        db = get_db()  # Obtén la conexión dentro de la función
        user_data = user.dict()
        result = await db.users.insert_one(user_data)

        #valdite user existin
        exiting_user=await db.users.find_one({"name":user.name })
        if exiting_user:
            raise HTTPException(status_code=400,detail="The user already existing in db")

        user_data["id"] = str(result.inserted_id)
        return user_data
        #return 200 ok
    except HTTPException as http_exc:
        # Maneja errores personalizados (por ejemplo, correo duplicado)
        raise http_exc
    except Exception as e:
        print(f"fail in the server {e}") #TODO guardar el log
        raise HTTPException(status_code=500,detail="Error internal of server")
        #return 500

@router.post("/movies/", response_model=MovieResponse)
async def create_movie(movie: MovieCreate):
    """
    Crea una película en la base de datos.
    """
    db = get_db()  # Obtén la conexión dentro de la función
    movie_data = movie.dict()
    result = await db.movies.insert_one(movie_data)
    movie_data["id"] = str(result.inserted_id)
    return movie_data

@router.get("/suggestions/{user_id}")
async def get_suggestions(user_id: str):
    """
    Devuelve sugerencias de películas basadas en las preferencias del usuario.
    """
    db = get_db()  # Obtén la conexión dentro de la función
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    preferences = user["preferences"]
    suggestions = db.movies.find({"genre": {"$in": preferences}})
    return [dict(movie, id=str(movie["_id"])) async for movie in suggestions]


#medir la latencia

