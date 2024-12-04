from fastapi import APIRouter, HTTPException
from app.schemas import ConcertCreate, ConcertResponse, TicketCreate, TicketResponse
from app.database import get_db
from bson import ObjectId

router = APIRouter()

# Rutas para conciertos
@router.post("/concerts/", response_model=ConcertResponse)
async def create_concert(concert: ConcertCreate):
    """
    Crea un concierto en la base de datos.
    """
    try:
        db = get_db()
        concert_data = concert.dict()

        # Verificar si ya existe un concierto con el mismo nombre y fecha
        existing_concert = await db.concerts.find_one({"name": concert.name, "date": concert.date})
        if existing_concert:
            raise HTTPException(status_code=400, detail="El concierto ya existe en la base de datos.")

        result = await db.concerts.insert_one(concert_data)
        concert_data["id"] = str(result.inserted_id)
        return concert_data
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"Fallo en el servidor: {e}")  # TODO: Guardar en el log
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.get("/concerts/", response_model=list[ConcertResponse])
async def get_concerts():
    """
    Devuelve una lista de conciertos disponibles.
    """
    try:
        db = get_db()
        concerts = db.concerts.find()
        return [dict(concert, id=str(concert["_id"])) async for concert in concerts]
    except Exception as e:
        print(f"Fallo en el servidor: {e}")  # TODO: Guardar en el log
        raise HTTPException(status_code=500, detail="Error interno del servidor")


# Rutas para tickets
@router.post("/tickets/", response_model=TicketResponse)
async def create_ticket(ticket: TicketCreate):
    """
    Crea un ticket asociado a un concierto en la base de datos.
    """
    try:
        db = get_db()
        ticket_data = ticket.dict()

        # Verificar si el concierto existe
        concert = await db.concerts.find_one({"_id": ObjectId(ticket.concert_id)})
        if not concert:
            raise HTTPException(status_code=404, detail="El concierto asociado no existe.")

        # Insertar el ticket
        result = await db.tickets.insert_one(ticket_data)
        ticket_data["id"] = str(result.inserted_id)
        return ticket_data
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"Fallo en el servidor: {e}")  # TODO: Guardar en el log
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.get("/tickets/{concert_id}", response_model=list[TicketResponse])
async def get_tickets(concert_id: str):
    """
    Devuelve una lista de tickets asociados a un concierto.
    """
    try:
        db = get_db()
        tickets = db.tickets.find({"concert_id": concert_id})
        return [dict(ticket, id=str(ticket["_id"])) async for ticket in tickets]
    except Exception as e:
        print(f"Fallo en el servidor: {e}")  # TODO: Guardar en el log
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.get("/tickets/available/{concert_id}", response_model=int)
async def get_available_tickets(concert_id: str):
    """
    Devuelve el número de tickets disponibles para un concierto.
    """
    try:
        db = get_db()
        count = await db.tickets.count_documents({"concert_id": concert_id, "status": "available"})
        return count
    except Exception as e:
        print(f"Fallo en el servidor: {e}")  # TODO: Guardar en el log
        raise HTTPException(status_code=500, detail="Error interno del servidor")
