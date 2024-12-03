import pytest
from pydantic import ValidationError
from app.models import UserModel, MovieModel

# Pruebas para el modelo `UserModel`
def test_user_model_valid():
    """
    Prueba que el modelo `UserModel` acepte datos válidos.
    """
    # Arrange
    valid_data = {"name": "Kevin", "preferences": ["acción", "comedia"]}

    # Act
    user = UserModel(**valid_data)

    # Assert
    assert user.name == "Kevin"
    assert user.preferences == ["acción", "comedia"]

def test_user_model_invalid_missing_field():
    """
    Prueba que el modelo `UserModel` genere un error si falta un campo obligatorio.
    """
    # Arrange
    invalid_data = {"name": "Kevin"}  # Falta `preferences`

    # Act & Assert
    with pytest.raises(ValidationError):
        UserModel(**invalid_data)

def test_user_model_invalid_type():
    """
    Prueba que el modelo `UserModel` genere un error si `preferences` no es una lista.
    """
    # Arrange
    invalid_data = {"name": "Kevin", "preferences": "acción"}  # `preferences` no es una lista

    # Act & Assert
    with pytest.raises(ValidationError):
        UserModel(**invalid_data)

# Pruebas para el modelo `MovieModel`
def test_movie_model_valid():
    """
    Prueba que el modelo `MovieModel` acepte datos válidos.
    """
    # Arrange
    valid_data = {
        "title": "Inception",
        "genre": "acción",
        "description": "Un ladrón de sueños",
    }

    # Act
    movie = MovieModel(**valid_data)

    # Assert
    assert movie.title == "Inception"
    assert movie.genre == "acción"
    assert movie.description == "Un ladrón de sueños"

def test_movie_model_invalid_missing_field():
    """
    Prueba que el modelo `MovieModel` genere un error si falta un campo obligatorio.
    """
    # Arrange
    invalid_data = {"title": "Inception", "description": "Un ladrón de sueños"}  # Falta `genre`

    # Act & Assert
    with pytest.raises(ValidationError):
        MovieModel(**invalid_data)

def test_movie_model_invalid_type():
    """
    Prueba que el modelo `MovieModel` genere un error si `genre` no es una cadena.
    """
    # Arrange
    invalid_data = {
        "title": "Inception",
        "genre": 123,  # `genre` debe ser una cadena
        "description": "Un ladrón de sueños",
    }

    # Act & Assert
    with pytest.raises(ValidationError):
        MovieModel(**invalid_data)
