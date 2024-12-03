from pydantic import BaseModel, Field
from typing import List

#schemas   definen campos se esperan su tipo y son obligatorio para request

# Esquema para usuarios
class UserCreate(BaseModel):
    # ... : indica obligatorio  case contrario None
    name: str =  Field(..., min_length=1, max_length=100, description="El nombre del usuario no puede estar vacío y debe tener entre 1 y 100 caracteres.")
    preferences: List[str] = Field( None,min_items=1, description="La lista de preferencias no puede estar vacía.")

class UserResponse(UserCreate):
    id: str

# Esquema para películas
class MovieCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="El título de la película no puede estar vacío.")
    genre: str = Field(..., min_length=1, max_length=50, description="El género de la película no puede estar vacío.")
    description: str = Field(..., min_length=1, description="La descripción de la película no puede estar vacía.")

class MovieResponse(MovieCreate):
    id: str
