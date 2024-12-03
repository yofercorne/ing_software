from pydantic import BaseModel
from typing import List

class UserModel(BaseModel):
    name: str
    preferences: List[str]  # Lista de géneros favoritos

class MovieModel(BaseModel):
    title: str
    genre: str
    description: str
