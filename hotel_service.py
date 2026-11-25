
from typing import Literal
from pydantic import BaseModel, Field


# 1. Define the 10 allowed hotel ticket categories
HotelCategory = Literal[
    "Booking_Issue",
    "Cancellation_Issue",
    "Checkin_Checkout",
    "Room_Cleanliness",
    "Room_Amenities",
    "Maintenance_Issue",
    "WiFi_Issue",
    "Food_Service",
    "Billing_Payment",
    "Customer_Service"
]


# 2. Define the required output structure
class TicketResult(BaseModel):
    category: HotelCategory
    summary: str = Field(min_length=5, max_length=250)


# 3. Define simple keyword rules for mock classification

CATEGORY_KEYWORDS = {
    "Checkin_Checkout": [
        "access card",
        "key card",
        "room key",
        "check-in",
        "check in",
        "checkout",
        "check out",
        "room not ready"
    ],

    "Room_Amenities": [
        "clean towels",
        "towels",
        "hair dryer",
        "air conditioner",
        "ac",
        "television",
        "tv",
        "pillow",
        "kettle",
        "refrigerator",
        "hot water",
        "facilities"
    ],

    "Maintenance_Issue": [
        "water damage",
        "wall damage",
        "repair",
        "broken",
        "leaking",
        "damaged",
        "maintenance"
    ],

    "Billing_Payment": [
        "refund amount",
        "incorrect refund",
        "refund is incorrect",
        "incorrect bill",
        "bill",
        "billing",
        "payment",
        "charged",
        "invoice",
        "extra charge"
    ],

    "Cancellation_Issue": [
        "cancel",
        "cancellation",
        "refund"
    ],

    "Booking_Issue": [
        "booking",
        "reservation",
        "confirmation",
        "reserved"
    ],

    "Room_Cleanliness": [
        "clean",
        "dirty",
        "dust",
        "bedsheet",
        "housekeeping"
    ],

    "WiFi_Issue": [
        "wifi",
        "wi-fi",
        "internet",
        "connection",
        "password"
    ],

    "Food_Service": [
        "food",
        "breakfast",
        "lunch",
        "dinner",
        "restaurant",
        "room service",
        "meal"
    ],

    "Customer_Service": [
        "staff",
        "manager",
        "receptionist",
        "luggage",
        "customer service",
        "rude"
    ]
}


# 4. Create the reusable ticket analysis function
def analyze_ticket(ticket_text: str) -> TicketResult:

    # Check whether the ticket is valid
    if not isinstance(ticket_text, str) or not ticket_text.strip():
        raise ValueError("Ticket text cannot be empty.")

    clean_ticket = ticket_text.strip()
    ticket_lower = clean_ticket.lower()

    # Default category if no keyword matches
    predicted_category = "Customer_Service"

    # Search for matching category keywords
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in ticket_lower for keyword in keywords):
            predicted_category = category
            break

    # Generate a short factual summary
    summary_text = f"The guest reports: {clean_ticket.rstrip('.!?')}."

    # Validate and return the result
    result = TicketResult(
        category=predicted_category,
        summary=summary_text
    )

    return result
