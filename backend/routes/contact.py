from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any

from backend.services.contact_service import create_contact, get_contacts

router = APIRouter(prefix="", tags=["Contact"])

class ContactRequest(BaseModel):
    full_name: str
    email: Optional[str] = None
    phone: str
    location: str
    message: Optional[str] = None

class ContactResponse(BaseModel):
    status: str
    message: str
    contact_id: int

@router.post("/contact", response_model=ContactResponse, summary="Submit a health screening inquiry")
async def submit_contact_form(contact: ContactRequest):
    """
    Store user consultation request into persistent backend storage.
    """
    if not contact.full_name or len(contact.full_name.strip()) < 2:
        raise HTTPException(status_code=422, detail="Full Name is required (at least 2 characters).")
    
    if not contact.phone or len(contact.phone.strip()) < 7:
        raise HTTPException(status_code=422, detail="A valid phone number is required.")

    if not contact.location:
        raise HTTPException(status_code=422, detail="Location is required.")

    try:
        record = create_contact(
            full_name=contact.full_name,
            phone=contact.phone,
            location=contact.location,
            email=contact.email,
            message=contact.message
        )
        return ContactResponse(
            status="success",
            message="Consultation request received successfully. A screening specialist will contact you.",
            contact_id=record["id"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error saving contact: {str(e)}")

@router.get("/contacts", summary="Get submitted inquiries")
async def list_contacts(limit: int = 50):
    """
    Fetch submitted contact consultation requests (Admin / Internal endpoint).
    """
    try:
        data = get_contacts(limit=limit)
        return {"count": len(data), "contacts": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error fetching contacts: {str(e)}")
