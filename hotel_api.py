
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from hotel_service import analyze_ticket, TicketResult

# Create FastAPI application
app = FastAPI(
    title="Hotel Help Desk Ticket Classification API",
    description="API for classifying hotel support tickets",
    version="1.0.0"
)


# Input structure
class TicketRequest(BaseModel):
    ticket: str = Field(min_length=1, max_length=1000)


# Home endpoint
@app.get("/")
def home():
    return {
        "message": "Hotel Ticket Classification API is running!"
    }


# Ticket analysis endpoint
@app.post("/analyze", response_model=TicketResult)
def analyze(request: TicketRequest):

    try:
        result = analyze_ticket(request.ticket)
        return result

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An internal server error occurred."
        )
