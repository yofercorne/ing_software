from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# Esquema para creación de conciertos
class ConcertCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="El nombre del concierto no puede estar vacío."
    )
    date: datetime = Field(..., description="La fecha y hora del concierto.")
    venue: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="El lugar del concierto no puede estar vacío."
    )
    genres: List[str] = Field(
        default=[],
        description="Lista de géneros asociados al concierto."
    )
    available_tickets: int = Field(
        ...,
        ge=0,
        description="Cantidad de tickets disponibles, no puede ser negativa."
    )

# Esquema de respuesta para conciertos
class ConcertResponse(ConcertCreate):
    id: str = Field(..., description="El identificador único del concierto.")

# Esquema para creación de tickets
class TicketCreate(BaseModel):
    concert_id: str = Field(..., description="El ID del concierto asociado.")
    status: str = Field(
        ...,
        pattern="^(available|reserved|purchased)$",  # Cambiado `regex` por `pattern`
        description="Estado del ticket: 'available', 'reserved' o 'purchased'."
    )

# Esquema de respuesta para tickets
class TicketResponse(TicketCreate):
    id: str = Field(..., description="El identificador único del ticket.")
    reserved_until: Optional[datetime] = Field(
        None,
        description="Fecha y hora límite para una reserva (si aplica)."
    )
