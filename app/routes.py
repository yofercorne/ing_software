from fastapi import APIRouter, HTTPException
from app.schemas import TicketCreate, TicketResponse
from app.database import get_db
from bson import ObjectId

router = APIRouter()

@router.post("/tickets/reserve", response_model=TicketResponse)
async def reserve_ticket(ticket: TicketCreate):
    """
    Reserve an available ticket for a concert.
    """
    try:
        db = get_db()

        # Check if the concert exists
        concert = await db.concerts.find_one({"_id": ObjectId(ticket.concert_id)})
        if not concert:
            raise HTTPException(status_code=404, detail="The associated concert does not exist.")

        # Check for available tickets
        available_ticket = await db.tickets.find_one({"concert_id": ticket.concert_id, "status": "available"})
        if not available_ticket:
            raise HTTPException(status_code=400, detail="No tickets available to reserve.")

        # Update the ticket to "reserved" status
        result = await db.tickets.update_one(
            {"_id": available_ticket["_id"]},
            {"$set": {"status": "reserved"}}
        )

        if result.modified_count == 1:
            return {
                "id": str(available_ticket["_id"]),
                "concert_id": ticket.concert_id,
                "status": "reserved"
            }
        else:
            raise HTTPException(status_code=500, detail="The ticket could not be reserved.")
    except Exception as e:
        print(f"Server error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/tickets/purchase", response_model=TicketResponse)
async def purchase_ticket(ticket: TicketCreate):
    """
    Purchase a reserved or available ticket for a concert.
    """
    try:
        db = get_db()

        # Check if the concert exists
        concert = await db.concerts.find_one({"_id": ObjectId(ticket.concert_id)})
        if not concert:
            raise HTTPException(status_code=404, detail="The associated concert does not exist.")

        # Check for reserved or available tickets
        reserved_or_available_ticket = await db.tickets.find_one(
            {"concert_id": ticket.concert_id, "status": {"$in": ["reserved", "available"]}}
        )
        if not reserved_or_available_ticket:
            raise HTTPException(status_code=400, detail="No tickets available to purchase.")

        # Update the ticket to "purchased" status
        result = await db.tickets.update_one(
            {"_id": reserved_or_available_ticket["_id"]},
            {"$set": {"status": "purchased"}}
        )

        if result.modified_count == 1:
            return {
                "id": str(reserved_or_available_ticket["_id"]),
                "concert_id": ticket.concert_id,
                "status": "purchased"
            }
        else:
            raise HTTPException(status_code=500, detail="The ticket purchase could not be completed.")
    except Exception as e:
        print(f"Server error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/tickets/cancel", response_model=TicketResponse)
async def cancel_ticket(ticket_id: str):
    """
    Cancel a reserved ticket and make it available again.
    """
    try:
        db = get_db()

        # Check if the ticket exists and is reserved
        ticket = await db.tickets.find_one({"_id": ObjectId(ticket_id), "status": "reserved"})
        if not ticket:
            raise HTTPException(status_code=404, detail="No reserved ticket found to cancel.")

        # Update the ticket to "available" status
        result = await db.tickets.update_one(
            {"_id": ObjectId(ticket_id)},
            {"$set": {"status": "available"}}
        )

        if result.modified_count == 1:
            return {
                "id": str(ticket["_id"]),
                "concert_id": ticket["concert_id"],
                "status": "available"
            }
        else:
            raise HTTPException(status_code=500, detail="The ticket could not be canceled.")
    except Exception as e:
        print(f"Server error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
